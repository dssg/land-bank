#!/usr/bin/env python

import cPickle, pprint, sys, csv, os
import psycopg2
import numpy as np
import pylab as py
import emcee
import scipy.sparse as sps
import scipy.linalg
import scipy.sparse.linalg as spslin
import scikits.sparse.cholmod

def get_data():
  ''' Get data from the database if necessary, or from cached file if it exists.'''
  if not os.path.exists('/home/tplagge/hedonic_data.pkl'):
    # Make a database connection and a cursor.
    conn = psycopg2.connect(host='localhost',dbname='landbank',user='postgres',password='postgres')
    cur  = conn.cursor()

    # Get a list of SFH transactions in 2012.
    cur.execute('''
      SELECT t.pin pin, t.amount_prime amt, a.sqft_bldg sqft, 
             t.date_doc dd, ST_X(t.loc) x, ST_Y(t.loc) y,
             a.garage_desc garage, a.year_built yb, a.ext_desc ext
      FROM landbank_data_transaction t
      JOIN landbank_data_assessor a
      ON t.pin=a.pin
      WHERE t.ptype_id=1
      AND t.purchase_less_20k=0
      AND t.buyer_type='I'
      AND t.seller_type='I'
      AND a.sqft_bldg > 0
      AND extract(year from date_doc)=2012
    ''')

    # Unpack the results.
    res  = cur.fetchall()
    pins = np.array([i[0] for i in res])
    amt  = np.array([float(i[1]) for i in res])
    sqft = np.array([float(i[2]) for i in res])
    dd   = np.array([i[3] for i in res])
    x    = np.array([float(i[4]) for i in res])
    y    = np.array([float(i[5]) for i in res])
    garage = np.array([i[6] for i in res])
    year_built = np.array([i[7] for i in res])
    ext = np.array([i[8] for i in res])
  
    # Store them in the cached file.
    with open('/home/tplagge/hedonic_data.pkl','wb') as f:
      cPickle.dump(pins, f)
      cPickle.dump(amt, f)
      cPickle.dump(sqft, f)
      cPickle.dump(dd, f)
      cPickle.dump(x, f)
      cPickle.dump(y, f)
      cPickle.dump(garage, f)
      cPickle.dump(year_built, f)
      cPickle.dump(ext, f)
  else:
    # Just read the data in from the cached file.
    f=open('/home/tplagge/hedonic_data.pkl','rb')
    pins        = cPickle.load(f)
    amt         = cPickle.load(f)
    sqft        = cPickle.load(f)
    dd          = cPickle.load(f)
    x           = cPickle.load(f)
    y           = cPickle.load(f)
    garage      = cPickle.load(f)
    year_built  = cPickle.load(f)
    ext         = cPickle.load(f)
  return pins, amt, sqft, dd, x, y, garage, year_built, ext

def calc_weight_matrix(x,y,dd,pins):
  '''Calculate the 1/distance weight matrix for the spatial
  autoregression component of the model.'''
  N = x.size
  W = sps.lil_matrix((N,N),dtype=np.float)
  for i in range(N):
    if i % 100 == 0: print i, N
    dist2 = (x-x[i])*(x-x[i])+(y-y[i])*(y-y[i])
    #dist2[np.where(dd > dd[i])] = np.nan
    dist2[np.where(pins==pins[i])] = np.nan
    dist2[np.where(dist2==0)] = 25.0*25.0
    sort_indices = np.argsort(dist2)
    if dist2[sort_indices[0]] == np.nan: continue
    sort_indices = sort_indices[0:10]
    sort_indices = sort_indices[np.where(~np.isnan(dist2[sort_indices]))]
    theseweights = 1.0 / np.sqrt(dist2[sort_indices])
    theseweights = theseweights / np.sum(theseweights)
    W[i, sort_indices] = theseweights
  return sps.csc_matrix(W)

def calc_prop_vector(sqft, ngarage, yrbuilt, ext):
  '''Make a vector out of the property characteristics we care about.'''
  N = sqft.size
  X = np.ones((N,5))
  X[:,1] = sqft
  X[:,2] = np.array([float(i[0]) if (i!=None and len(i)>0 and i[0] in ['1','2','3','4']) else 0 for i in ngarage])
  X[:,3] = [float(i) - 1900 if i!=None else 0 for i in yrbuilt]
  X[:,4] = [1 if i=='Masonry' else 0 for i in ext]
  return X

def calc_logl(params, Y, X, W, XTXinv):
  # params = (beta, error)
  # beta = (c_int, c_sqft)
  # X_i = (1 sqft_i)
  # W = weight matrix

  # log(price) = S beta X + S error
  # S = (1 - lambda W)^(-1) 

  c_int, c_sqft, c_garage, c_yrbuilt, c_ext, lam, var = params
  if c_int > max(Y): return -np.inf
  if var < 0: return -np.inf
  beta = np.array([c_int, c_sqft, c_garage, c_yrbuilt, c_ext])
  N = len(Y)

  # Compute 1 - lambda W
  one_minus_lamW     = sps.identity(N) - lam * W
  # Cholesky decompose it for inverse and determinant computations.
  one_minus_lamW_inv = scikits.sparse.cholmod.cholesky(one_minus_lamW)
  # Compute the residuals: Y - (1-lambda W)^-1 X beta
  R = Y - one_minus_lamW_inv.solve_A(np.dot(X,beta))
  # Compute chi-square: -0.5 R cov^-1 R^T
  # where cov = (1-lambda W)^-1 * I * var
  # (so cov^-1 is (1-lambda W) * I * (1/var))
  chisq = -0.5 * np.dot(R, one_minus_lamW.dot(R.T)) / var
  # Compute log(det(cov))
  #   = - log(det(cov^-1))
  #   = - log(1/var^N det(1-lambda W))
  #   = N log(var) - log(det(1-lambda W))
  # The last term is computed via the Cholesky decomposition.
  logdet = N*np.log(var) - one_minus_lamW_inv.logdet()
  # The log likelihood is -0.5 log(det(cov)) + chisq.
  logl = -0.5 * logdet + chisq

  # Print debugging messages
  print chisq, -0.5 * logdet
  print c_int, c_sqft, c_garage, c_yrbuilt, lam, var, logl

  # Return the result unless it's nan.
  if np.isnan(logl): return -np.inf
  return logl

if __name__=='__main__':
  
  pins, amt, sqft, dd, x, y, garage, year_built, ext = get_data()
  X = calc_prop_vector(sqft, garage, year_built, ext)
  W = calc_weight_matrix(x,y,dd,pins)
  Y = np.log(np.array(amt))
  XTXinv = scipy.linalg.inv(np.dot(X.T,X))

  ndim = 7
  nwalkers = 50
  p0 = [(np.random.rand(ndim)+0.5)*\
    np.array([11.0,0.0006,0.01,0.01,0.01,0.1,0.35]) for i in xrange(nwalkers)]
  sampler = emcee.EnsembleSampler(nwalkers, ndim, calc_logl, \
            args=[Y, X, W, XTXinv],a=3,threads=3)
  print 'Burning in'
  pos,prob,state = sampler.run_mcmc(p0, 500)

  sampler.reset()
  print 'Running MCMC'
  pos,prob,state = sampler.run_mcmc(pos,1500,rstate0=state)

  af = sampler.acceptance_fraction
  print 'Mean acceptance fraction:', np.mean(af)
  maxprob_index = np.argmax(prob)
  params_fit = pos[maxprob_index]
  errors_fit = [sampler.flatchain[:,i].std() for i in xrange(ndim)]
  print params_fit
  print errors_fit

  f=open('/home/tplagge/hedonic_chain.pkl','wb')
  cPickle.dump(sampler.flatchain,f)
