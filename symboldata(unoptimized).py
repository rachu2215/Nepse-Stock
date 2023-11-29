import csv
import requests
from bs4 import BeautifulSoup

cookies = {
    "ASP.NET_SessionId": "gi4gozrjifu4xkp3x0uh4bmz",
}
headers = {
    "authority": "merolagani.com",
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "no-cache",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    # 'cookie': 'ASP.NET_SessionId=gi4gozrjifu4xkp3x0uh4bmz',
    "origin": "https://merolagani.com",
    "referer": "https://merolagani.com/CompanyDetail.aspx?symbol=ACLBSL",
    "sec-ch-ua": '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
    "x-microsoftajax": "Delta=true",
    "x-requested-with": "XMLHttpRequest",
}
input_params = input("Enter the symbol: ")
params = {
    "symbol": input_params,
}

data = {
    "ctl00$ScriptManager1": "ctl00$ContentPlaceHolder1$CompanyDetail1$tabPanel|ctl00$ContentPlaceHolder1$CompanyDetail1$PagerControlTransactionHistory1$btnPaging",
    "ctl00$ASCompany$hdnAutoSuggest": "0",
    "ctl00$ASCompany$txtAutoSuggest": "",
    "ctl00$txtNews": "",
    "ctl00$AutoSuggest1$hdnAutoSuggest": "0",
    "ctl00$AutoSuggest1$txtAutoSuggest": "",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$hdnStockSymbol": "ACLBSL",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$hdnActiveTabID": "#divHistory",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$StockGraph1$hdnStockSymbol": "ACLBSL",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$ddlAncFiscalYearFilter": "",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$PagerControlAnnouncement1$hdnPCID": "PC1",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$PagerControlAnnouncement1$hdnCurrentPage": "0",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$PagerControlAnnouncement2$hdnPCID": "PC2",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$PagerControlAnnouncement2$hdnCurrentPage": "0",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$txtNews": "",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$PagerControlNews1$hdnPCID": "PC1",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$PagerControlNews1$hdnCurrentPage": "0",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$PagerControlNews2$hdnPCID": "PC2",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$PagerControlNews2$hdnCurrentPage": "0",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$txtMarketDatePriceFilter": "",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$PagerControlTransactionHistory1$hdnPCID": "PC1",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$PagerControlTransactionHistory1$hdnCurrentPage": "2",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$PagerControlTransactionHistory2$hdnPCID": "PC2",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$PagerControlTransactionHistory2$hdnCurrentPage": "0",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$txtBuyerFilter": "",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$txtSellerFilter": "",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$txtFloorsheetDateFilter": "",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$PagerControlFloorsheet1$hdnPCID": "PC1",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$PagerControlFloorsheet1$hdnCurrentPage": "0",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$PagerControlFloorsheet2$hdnPCID": "PC2",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$PagerControlFloorsheet2$hdnCurrentPage": "0",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$ddlFiscalYear": "",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$ddlSectorFilter": "0",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$PagerControlAgm1$hdnPCID": "PC1",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$PagerControlAgm1$hdnCurrentPage": "0",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$PagerControlAgm2$hdnPCID": "PC2",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$PagerControlAgm2$hdnCurrentPage": "0",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$ddlFiscalYear1": "",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$ddlSectorFilter1": "0",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$PagerControl1$hdnPCID": "PC1",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$PagerControl1$hdnCurrentPage": "0",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$PagerControl2$hdnPCID": "PC2",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$PagerControl2$hdnCurrentPage": "0",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$ddlFiscalYear2": "",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$ddlSectorFilter2": "0",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$PagerControl3$hdnPCID": "PC3",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$PagerControl3$hdnCurrentPage": "0",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$PagerControl4$hdnPCID": "PC4",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$PagerControl4$hdnCurrentPage": "0",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$PagerControl5$hdnPCID": "PC5",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$PagerControl5$hdnCurrentPage": "0",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$PagerControl6$hdnPCID": "PC6",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$PagerControl6$hdnCurrentPage": "0",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$PagerControl7$hdnPCID": "PC7",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$PagerControl7$hdnCurrentPage": "0",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$PagerControl8$hdnPCID": "PC8",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$PagerControl8$hdnCurrentPage": "0",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$PagerControl9$hdnPCID": "PC9",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$PagerControl9$hdnCurrentPage": "0",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$PagerControl10$hdnPCID": "PC10",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$PagerControl10$hdnCurrentPage": "0",
    "__EVENTTARGET": "",
    "__EVENTARGUMENT": "",
    "__VIEWSTATE": "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",
    "__VIEWSTATEGENERATOR": "982A0BEA",
    "__EVENTVALIDATION": "H8ImrIXs6FhCfuF6JX/jX6t3XagzqGdl6oEWlnIir9av4OQx8o/aMgBLzAwL4BSnx0zBIl1ECK+J28lXFPnz8KlyYYjiX7/gaSCyfkLWKGm4+U2o9eSBSVMWPN3cBZcsjN2Rmnasw7eGhbgVgD3WOAk9WvP4bB4OTLaYIy6ZVCxjIaJljCpzbt/aUXRpMwnTZXtk7Z6yNfCFTIZ/qISNNQL3c0vE9k+9JY/1SRzuQP+6fRjOCt6b7jPYqOTggvZ6qUJRt/R7AgkHhosUUEjF1MV2tCMC9aKSI1efMGFDLEGdVf0Jv+A98F+eNm0nN2mWdyEhSIH4ODDhEDaQTbmXF1IIowghyW89A8fRoicMWqYjlfvdI9TsjC/6PPFp+Zp6snNBM9kZw1raF0faaiPYBzK05FEaX1SVf3EeGB6g48ELRMZ1AD6ut2axjSWY490y8gn4NJiEiDuHWr0FkQ8tbGk65u8TD/QGlbRaw3sOvJOHx4II6v1Sghg6tlMAG5lsBDrwxjqo3C/fwWM7/1wRLwojXpOaUP1TXmDtpgU575fOEnfVcnLSQxmFupJQXqShEqUAFyoXMFrhm2c+tQOnaRq0vBKZL/GRSnyWODJuDtsk60SNhNayzVmn/ssh65hPNo/poOQkUdYBF2uEl/etAo1UlGqqYKInotac9tAZd7uvceucZ+bVsT7ZaApkqWDsvA7MG582Yk3FvzPLAHkyQnK8GxiG1ljwmibcfN+hYe26TQxQ/fSfHaW8G5PlSReBP9P2KsuTkoIyjS5SsqunDfH6Tf0ruveYE8YxwJ155sjlVe9vsWfr1s9B9DzxszR4LD+f2tm7kq0oQrSEgCYoH541Xysog55GP1IDmxj/OTSyVUpwr6MiwcvJbbyDkz+jzrqfO4FPL3hXTx9dOPnEFB5Bnp3WaubR7JqskgKpLxxDU/NVIuRW6CRa6JBO/rNkRIsp+++8KE9td7OEKyhqx7Ul5ut/vXPr//mHKWysJfYJMvQaj3wXj3cSWkuDuOtCf/aTrDmnCCH5Kjy7Y998I5KY0975k+pBasSTvc/52uH17Woy89Ni0Nd0Ku0f8CZS2Y67uHBdmHgueP0sknLVGYIxt4vUVzqCRBlpbsrE8GL+WB6tBGPhewUbzcrm9opWUjM/UfUxFOXagbCtha9rcYJ7mYDfsbhu3jmwiibuLW4WbjYh9PO/sPqykCSe4BMs3MGxCEd/BY8SKXG/jhGGmnVP+2cKqGlmYjRcG8dROqIpDIDj4Wd6+dx9yIfTJPKa7j8qOLrCbj1Uv8S6MD4BUEOONQdIYD971q7mz+Yygk+Taqx0+enfnFupQasIv6mUDxqRYyIEQGJ5h8jp6AaxbOe0W8d1l+YOcEPGPnMoXA60Gas9KVv9nvRnH4QjguqzwU7jiHzstPbaSaa7+36KLB3yKx9vtDWu9Q7L1JvCJp3so0ld/wkyQNHy8j2eqh+2UipGEKjEyXEPhtxJXGaaKYXaucVfdCNBHsSp5284BIX5sHeM++IDN78aqGsMypTSX/Fza6nTentmFF9qRqS2Oxarb11rVcKjP2YG2GGu0fJErcBcqbEKGGpwCYCEjpWDOzfWW14jA9K/p95MGNIeoyeV2PF1j0GLhCKyfNx3roLB9DGHYs+9CBxhrWrYdIEoss+CmBjJU4JEFQma2BCIkT6kwToZJD1K52CfirdZNS3V/R03TAYFMPmCsMNS4OLzczJkqqo/VjfrO6e42giVud9ynDgfDNr/GW52cjX3p90b+zgELfps9NBcHyQLU/jzDrpiifgZCje7q+2wNPByfvioQdKTooQEsRQwHMP5Yctywb37ovk6qaZO2jZDJpJfF1LbdH0avzYgelMysRAHNH6VyOF0GmL2xG8cne0tnsc41En2CkAgWMIXB8KMRf5htHu6mmXvzuQ1dYwXERadptyo7rjn10g/LfatPG9NkH4jDXXyAmb+SetdSt8edeRDkisUZNPlyAj5rpFS/HJxreEJRXX6ZCOO3mifzxkYZ8neXanLoXONeKcXMvlshzrOSBg8PDECWsuXUxMBjH8Ss44apjItUWI9Yr7eTVGIvsjwbE+7XYj/5Krbu79qpksoyaiZjczhMdGWxf65WY5LlGE31yn2atw3XXfny8C4xWFLVk913j3UWCAvUO6Sy3tB+9pYJl7p97TrYRfdfpxTMOEmhTa3PQ2nt5y/YWmiEuqnHQ3XlnRirwHvi19Weyf+unWm15chYL4HGSJvohT8DHVI6J1YT8ilHMw2POvJ7HHVsV932JANU5nOKbM4E1mMHbEoHbq7Ti+uf3pHRsxA5zQHFiHc8OMdr0cHT0wEevjO3bEmvJbFJRUxa5vuLs5xZNZtxFMFmkb0Bc3yY2b2zLQ1wGrsdGty8QyMM3E8VIj55RmRP+ABKe4THxKHXhPtEQarcx2OO5o9L/wdF+QN6Kba/LHAkW0uOH5NtYT3l+Adj3eZZNg9nEzqslWIPNZRfkE0n9O6BNxR6GEjKraqMzKOofhP0LAMuJjiQ2cuzzFhODqsfPuONzAeUdCHDq1UzPNsEl/tCekT1CBxgHqbu4WFR9QUYBpbIB4+m9yAndZ/LcNSkx46kiXf+4KQCRvLQnaN83LBfONTJWpiaEb7s0H4BVledx+sDWAb2N3d3qYm/2pE2VbRliKJVq3x/2kfJaiWLXJ4LsN5ERZQdmjHU+SbilHxwS44oGgT3t27p3y8/Wmr/4bwdBFrwo4+JT/WlNn9QLnGx+pN6imCNLjMlCIpYoCcZFm4wlj4LN02qUwOLneBPh359zdgcPOdCMAMZdGt+7MAjnhvSXmq1CR3ZgL6HNijEklNVEpPju9WsERR+8mmes+4pL81tEsN3eN6ddoX9cAXkPRONAX/ejJWt9osyULPU+WP1001Ano7249HeYMLhVh8RKUsh2ECNNvVK6Hffn3xV0uIHoSQ4C2r03GkZbC4JtegcLBw7vKYWA0DTaNrgdbMejotXyh8LV/WnbdHASDK8jR19C4ARcQjzh4FgiRKB9x2iLRNeHNT1eKxLJF4LZo/cCnG2vxEooBF9rxGwBQNlU4I9SDZo20LDFE/kHwOKdl7vE7SfiWqYwSsz7bm3Cg8RfTMZS6jSkIIFbZM+5VMnDPosf3heaF7MvSNGvPIxXLkHH8ymfUKCyanRW5ClmlduG8BD3Kr3rklBG22FV00TEHKw7TkrzcPqyiZe9u+rkp92ZnbIWSHr7dLVV4uk11puSOwCrfpivV7sw20KL7a6uPQb3zlPZf73vlNNNpaE7JntcwVfMgEtKGhpAXJVPV1iLeruT4ooTkhGC8Z8oSRJaLLioh30tDppj5pbzBnLrZlBMB+PPhfMUxdKq8xLLNOMMj++VPhXctZoxQi+tyICfFW3EJZL2t3CZwKBD1kPs8c/fbT0490rk92G7PA6RDbl8iu4MmQ/jUSXCEeIH6XgBuVYN3m+3XYkYyrc8YK6CgIe06CuJqsV54n9xOXBgIOxZLYd6WrHHUHP3DiBzsBrWPNtYBY5wn18g9XsCt7ybzE2GVRnPn01QV7ah2tbCLtdgrEeVhcPFZNQcucno7oRHI4OwzXCU7MLB4T+pBGkpsc7qyRzDysfYpqxhW4Kz77DU3cs98Cuw58OuchuLGEWZ4nkczkvRNLPUG2DrFVH6VGd+JxVcWJ1bOWJxjoPmSdoI7+fi123YgmCMZ/a76xhdl/nLXCLfAxgSkMlKjmv6NwEaKkggTh27OhiZOMn2ourZy4o2Qia28zKkBFBinHnlcT9n/fundWCPU7nuBPG8KLOdhYXlAlgBrSW5xAXtwuhiKxmc9YNzLHZZIkTUv7TQAUrkUGfUzLE60YkDMPrDNDaQubah240ao/nebAJS3b9yZMoDMGQ3zagVLLx0Q4nyHQbSmskjUXPUdxvnY1lyo7TBh+354oEurIiXPFSOjUDdQSfy4OkPvreh3fNEe/RFC0NUhMDmKcLigQvhALMbL0IZz1t5gZmvB0va+zj5UXM10RFhs2cMtwyjtCWc/88oeuIuUrOzwcu4+3IzHxhMcYJEBoPypr/2fzrB1Ri43GOBGSveNEZAJZ9wfHyRShqYmu1b36qFd8Z6MKYYnCaafIclfimO12+YMf7rrYXgdSWR/04DMoqpJsTEUA/K9CN1m896Xnbdewd/IF8GV1q32MbGDPwP0HmKmb3GqF9SOrrP45Kbn7/dVoufQQcN1MbdAHXQ6d2FCpeMWiDLlX/F8UFgYcw3b7t/ZvyB2HcCKTQjbeK5VBWZqGVD+D2VuHJFhnb3FKZuYEZ4PO3ZVmxzC6yMw2sYfVuG7TnQgnNriYKi5KlXYxq0nsZGGio125nGQcKDeyKLKTKE12gPh8HNdwsUccpOFzuW+dmp0rcKiXEtxy1UbSM51GikQZpi/v8sZoettBo787CoTa2A5H5F302pvLOAwgepsspZeFd2psX2iLVWibzq1FxrlFjxHq1vuYrX7OiNXs0w29b4u6l9Wq10phfFu1kH5PE5txcGRS02RPfNr/Ab46nZcn0RhvNgwNFN3cRtf5HOJcJ2GG26rS3XMyE8kKkTVBZNt5ly2kHIGvgVbxtGhT1837u4/90xJ1IhP6AlML/TGFHNRMo2B9TbhznChCO4ck5BWf6bzGTK6aFtnEfflF2ambjB+YqjF0AZyvAugenhtYBHpko6oybxJzvAkjk8ZoxGRY6rbSe2kX5uhSMAfIwLQV26W6zzPYzTkaqFnmEyVsgbHwYR5nNGfb2K1pKUsCCMmUAfJlWXVkUvOkmwVeblYl7LBDMqimnYxMLQCqpgzURZtE6UTnVOfic67c811OULfP8KVVOh8mPc5Hs5IdYQ4BusQKooin4jJBaNyMb/iDWPvcmwfAzHcniV5db5OHeW8WHySPgkQ6A5zmDQoGBm275WxAf1e38NMFkfEC2rg9hIa/N/DMdE5fH0Txa+YQvKJqQ9jCcefsQrGr/TX1MTQFtAQj1Ht2y38IxTIleGHgRxftWjccF2rf2IpldsR+TrU1W7Xe1NEFz9gjeTvFA9Ozr1I+o8FJLtGCg3OY3q2NlabwfD3Z5jWY0yJcFqLmRo4+tfJRsVLbWQjvoEO4wtEIL9zjlKSyCmmn0cu1BYycjyKF1L6xPLA+kXmOEuJydyboM0fGftvrxwijBwhRLApL1cSKODfzHo4j8G54C+zkXxoOYNsF0/UZillOI3su4HS+/V8p7sQvOJWk/3gX9tQZvdwQ9XhshSAf1F1q9b3Y4VVzqqVDbqB1ccuCPcWDbuNdVSLsvpUHJsK6Y9/DWI5ApS9CL7ZhJZE8Xsfug1Ph+dG2JDfPyKb7gPX/AipjhkLNVUJ8guo74n/G346N1uX0t1bytD/4suCiKmSfBOIfkYhDV7qsZ8zEzpcAIlQy6L5ynqJ0yPfxaSissQSdvNy3ergySCq9fMAhuHf/vTT6MO7SaNtPhVXJn6wW/AYWqA10qmfNAQtgh369XdcxZnP/rq6r8MjTPyJHAdCC5lq2h10hsUKNLr9040bYQWolcKdEppbk/5bD5zYJpEVushv+GaXVdK/pejOnloHwFCihkCgFSV4p1m55qRdma3gNq2n5iOwLDXtYYHPPz8HR2XxjdwePw9ab7Moq/dMqAmyGs3tgm6HRDtLL3knuZzwvQ5N4cJdVO+NJCD6Wz2K0KeBHpmWIF6K6qlbT9NkM04B/wnEN0zLGyMT8d3T0eqSmAM9o87Uz5Vd459RK3kG8+/Nd+oE+AfqkucFzKvTbIjPsVMOFeViDOWtgpQWTJJi0PWErti7OXROaxogpAWJY/HhMguGVKyQY95HCP/6dYoRxNboGa0Kae4JpbSZtCGMw1pH34PJkIgUrYliCiF2JGIsdLPZ9YPuNq7FL5BlWuWp6uSTznHzQLZ++ppJtJdGpR27TZxRM3UjcTryYTfL+w2DpaGY5UUMbOOwIBY7WPJWewyHN2leKsxXjPEdIE2yS7ZEqljt7AtTtrVcs+UkigAxaS7o0+DfMpnlLOpss/2J0LnlWlxpVLYOBbR+Z1zvCxTZFE4+W0tXp+p+UVdAC074HNMJpRDMbEQa2MQ0VM6R3bdoUZuzhRGRqFQ6GIFHV/tj+Bt7+m39TgLSQzE5C5kWJeduepcL0bI8LuowC88/NWI9YSSoerGam2I+rtBTaq2rI7LBMBFhFNLGP/iMUnZGOGcjimPlw5F4J0EwfqYSRNpRMXwqWlqaNkNDA/XDzryibYERIHzQESJmSIybA/FwJbWGdQNEKtetZOt9U534dmQBq1+LBhRbW8ivaKOzpEpJGJkHRxXQO2DuYP7Uq7jhVffXVu0+wbBh1nleH/C59XQd70b8eU4f2LcCOzcTPhUMFGQWNKqImf3ZM3slZRNH+yy85GNSD/J4yDQY3ig/kpNYPx+3dmCYuVGFu67h4Zhidc/yn7bUWysgEVfcPFqhkkK99IDlawu6HCbY5LBGUqm4aP20EMfWBTPphXHKGKfEz/DRtN3ab8MZdeVUjtb9MyieFvaUSA2aMCgdEP+xQtPoooe0iePYyOAiF+OgkewSF4D2oD0aI13PwqPRrtWXmKBTGlSrFIVGLpqj67MSRuVlu9TnJqAp1YKaZi56ON9UKGhxP/9opgLXjUh8p00M1o2OxMcI/6VqvoheB5JJmHLVuW8aqYjB9+w0/xYqOCAIabFUE6IRG54dAWSagt60J1gxQgF4tWahEA+67U6Ua7iZJQZM1ZxaIEufCEdd0bAGyYqJlA9+xsZXgRxs5zpLqp9PWtApssqIh8wx8MaeFtKb/lSqh5nLK+o2FeOUzlSYpsdiRX4PCaY2OtMzdnDx5jT5rS+r8K7o3EqK75FoPGXejoJBDitHf1BRFENN+SAE0uoYPq4emPlet5/7n",
    "__ASYNCPOST": "true",
    "ctl00$ContentPlaceHolder1$CompanyDetail1$PagerControlTransactionHistory1$btnPaging": "",
}

res = requests.post(
    "https://merolagani.com/CompanyDetail.aspx",
    params=params,
    cookies=cookies,
    headers=headers,
    data=data,
)


soup = BeautifulSoup(res.text, "html.parser")


table = soup.find_all("table")[2]

headings = []

for heading in table.find_all("th"):
    headings.append(heading.text.strip())

data = []

for row in table.find_all("tr")[1:]:
    data.append([td.text.strip() for td in row.find_all("td")])

dicts = []

for row in data:
    dicts.append(dict(zip(headings, row)))


with open(f"{input_params}.csv", "w") as f:
    writer = csv.DictWriter(f, headings)
    writer.writeheader()
    writer.writerows(dicts)

print("Done")
