import matploblib.pyplot as plt


fig = plt.figure(figsize = (5, 5))

ax = fig.add_subplot(111)

ax.set_title("foobar")
ax.plot(foo)
ax.set_xlabel("X axis")
...


plt.savefig(...)



sf['land_assmt_11_psf'][sf['CA_name']==CA_names[0]].hist(),
grid(True)
title('Land size and price')
ylabel('count')
xlabel('$')

subplot(222)
sf['bldg_assmt_11_psf'][sf['CA_name']==CA_names[0]].hist()
grid(True)
title('Building size and price')
xlabel('$')


subplot(223)

sf['Msqft_land_11'][sf['CA_name']==CA_names[0]].hist()
grid(True)
ylabel('count')
xlabel('10^3 sf^2')

subplot(224)

sf['Msqft_bldg_11'][sf['CA_name']==CA_names[0]].hist()
grid(True)
xlabel('10^3 sf^2')

tight_layout()

figPath=baseDir + CA_names[0] +'.png'
#savefig(figPath)

#clf()
