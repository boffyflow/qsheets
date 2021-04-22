# Settings for qsheet python script

# Market holidays. Text file containing a list of dates
# one YYYY-MM-DD per line 
HOLIDAYS = 'tsx_holidays.txt'

# Pause time for each Google Sheets update. Required as google only allows 
# a fixed number update per minute. Default 5 seconds should be safe
# value is in seconcds
SLEEPTIME = 5

# requested returns for the years
# 0 = last trading day from current date
# 1 = last trading day one year from current date
# etc.
RETURNYEARS = [ 0, 1, 3, 5, 10]

# Document must have a name and can have a quote sheet, sparkline sheet and returns sheet
# DOC1 = { 'name':'Test1','quotesheet':'Data','slsheet':'Sparklines','returnsheet':'Returns'}
# DOCS = [ DOC1]
# Instructions for above example:
# 1. Create a Google Sheets document named "Test1"
# 2. Share document with python user account
# 3. Create sheets named "Data", "Sparklines" and "Returns"
# 4. Add ticker symbols into column A, starting at row 2 for each sheet. 
# Note: Row 1 goes not get updated in able to add labels
# For example:
#      A        B          C        D       E
# 1
# 2    T.TO
# 3    SU.TO
# 4    TD.TO

# Multiple documents are also supported
# Just uncomment lines below and ensure the list of docs is modified accordingly

DOC1 = { 'name':'Test1','quotesheet':'Data','slsheet':'Sparklines','returnsheet':'Returns'}
#DOC2 = { 'name':'Test2','quotesheet':'Data','slsheet':'Sparklines','returnsheet':'Returns'}
#DOC3 = { 'name':'Test3','quotesheet':'Data','slsheet':'Sparklines','returnsheet':'Returns'}
# list of documents
DOCS = [ DOC1]
#DOCS = [ DOC1, DOC2, DOC3]
