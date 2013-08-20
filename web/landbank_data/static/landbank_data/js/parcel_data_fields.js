// *Ordered* list of parcel data fields that may appear in the detail pane
var parcelDataFields = 
[
  {
    "id":"summary"
   ,"heading":"Summary"
   ,"fields":
      [{
        "id":"address"
       ,"display":"Address"
      },{
        "id":"pin"
       ,"display":"Property PIN"
      },{
        "id":"property_type"
       ,"display":"Property Type"
      }]
  },{
    "id":"mort"
   ,"heading":"Mortgage History"
   ,"fields":
      [{
        "id":"mort_date"
       ,"display":"Date Filed"
      },{
        "id":"mort_amt"
       ,"display":"Loan Amount"
      },{
        "id":"mort_borrower"
       ,"display":"Borrower"
      },{
        "id":"mort_lender"
       ,"display":"Lender"
      }]
  },{
    "id":"fc"
   ,"heading":"Foreclosure History"
   ,"fields":
      [{
        "id":"fc_date"
       ,"display":"Date Filed"
      },{
        "id":"fc_plaintiff"
       ,"display":"Plaintiff"
      }]
  },{
    "id":"txn"
   ,"heading":"Transaction History"
   ,"fields":
      [{
        "id":"txn_date"
       ,"display":"Last purchase"
      },{
        "id":"txn_amt"
       ,"display":"Sale price"
      }]
  },{
    "id":"vac"
   ,"heading":"Vacancy Reports"
   ,"fields":
      [{
        "id":"vac_request_date"
       ,"display":"Last 311 Request"
      }]
  },{
    "id":"scav"
   ,"heading":"Scavenger Sale History"
   ,"fields":
      [{
        "id":"scav_tax_year"
       ,"display":"Tax year"
      },{
        "id":"scav_tax_amt"
       ,"display":"Tax amount"
      },{
        "id":"scav_tot_amt"
       ,"display":"Total amount"
      }]
  },{
    "id":"brown"
   ,"heading":"Brownfield Status"
   ,"fields":
      [{
        "id":"brown_grant_types"
       ,"display":"Grant types"
      }]
  },{
    "id":"cmap"
   ,"heading":"CMAP Status"
   ,"fields":
      [{
        "id":"cmap_name"
       ,"display":"Organization"
      },{
        "id":"cmap_status"
       ,"display":"Status"
      },{
        "id":"cmap_area"
       ,"display":"Area"
      },{
        "id":"cmap_desc"
       ,"display":"Description"
      },{
        "id":"cmap_url"
       ,"display":"Website"
      },{
      }]
  }
]
