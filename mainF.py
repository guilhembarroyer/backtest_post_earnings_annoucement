import asyncio
from backtestF import extraction

async def main():
    earnings=[1,2,3,4,5,6] 
    combinaison=None 
    univers=['AAON', 'AADI', 'AAL' ,'AAPL', 'ABCB', 'ABCL', 'ABEO' ,'ABOS', 'ABSI', 'ABUS', 'ACAD' ,'ACB', 'ACCD', 'ACET',
'ACGL', 'ACHC' ,'ACHL' ,'ACHV' ,'ACIU', 'ACIW' ,'ACLS', 'ACLX', 'ACMR', 'ACNB', 'ACON' ,'ACRS', 'ACST', 'ACT', 'ACTG', 
'ACVA', 'ACXP', 'ADAP', 'ADI', 'ADIL' ,'ADMA', 'ADP' ,'ADPT',  'ADUS' ,'ADV' ,'ADVM', 'AEHL', 'AEIS',
'AEMD', 'AEP', 'AEYE' ,'AFCG', 'AFRM', 'AFYA' ,'AGIO', 'AGNC', 'AGYS' ,'AHCO', 'AHG' ,'AIP' ,'AIRG', 'AIRS', 'AKAM',
'AKBA', 'AKRO' ,'AKTS', 'AKYA', 'ALAR', 'ALCO' ,'ALDX', 'ALEC', 'ALGM', 'ALGS', 'ALGT' ,'ALHC', 'ALIM',
'ALKS', 'ALKT', 'ALLK', 'ALLO',  'ALLT', 'ALNY', 'ALRM', 'ALRS', 'ALT', 'ALTO', 'ALVO', 'ALVR', 'ALXO', 
'ALZN', 'AMAL', 'AMAT', 'AMBA', 'AMD', 'AMED' ,'AMGN' ,'AMKR', 'AMLX', 'AMPG', 'AMPH' ,'AMRK', 'AMRN',  'AMSF', 
'AMTX', 'AMWD' ,'AMZN', 'ANAB' ,'ANDE', 'ANEB', 'ANGH' ,'ANGO' ,'ANIK', 'ANIP', 'ANIX', 'ANNX', 'ANSS', 'ANTE' ,'ANTX' ,'AOSL',
'AOUT', 'APA', 'APDN', 'APEI', 'API', 'APLS', 'APLT', 'APOG', 'APPS', 'APRE', 'APTO', 'APVO', 'APWC', 'APYX',
'AQB', 'AQMS', 'AQST', 'ARAY', 'ARBK', 'ARCB', 'ARCC', 'ARCT', 'ARDX', 'ARGX', 'ARLP', 'AROW', 'ARQT',
'ARTL', 'ARVN', 'ARWR', 'ASLE', 'ASMB', 'ASML', 'ASND', 'ASPS', 'ASTE', 'ASUR', 'ASX', 'ASYS', 'ATAI',
'ATEC', 'ATEN','ATER', 'ATEX', 'ATGE', 'ATHA', 'ATHM', 'ATI', 'ATKR', 'ATLC', 'ATNI', 'ATO', 'ATOM',
'ATOS', 'ATR', 'ATRA', 'ATRC', 'ATRO', 'ATSG', 'ATXI', 'ATXS', 'AU', 'AUB','AUDC', 'AUGX', 'AUPH', 'AURA',
'AUTL', 'AUUD', 'AVA', 'AVAH', 'AVAL', 'AVAV', 'AVB', 'AVD', 'AVDL', 'AVDX', 'AVGO', 'AVGR', 'AVIR',
'AVNS', 'AVNT', 'AVO', 'AVT', 'AVTE', 'AVTR', 'AVTX', 'AVXL', 'AVY', 'AWI',  'AWR',
'AX', 'AXDX', 'AXGN', 'AXL', 'AXNX', 'AXON', 'AXP', 'AXS', 'AXSM', 'AXTA', 'AXTI', 'AY', 'AYI', 'AYTU',
'AZ', 'AZN', 'AZO','AZPN', 'AZTA', 'AZUL', 'AZZ', 'B', 'BA','BABA', 'BAC', 'BAK', 'BALL', 'BALY', 
'BANC', 'BANF', 'BANR', 'BAP', 'BASE', 'BB', 'BBAI', 'BBD', 'BBDC', 'BBIO', 'BBLG', 'BBSI', 'BBU',
'BBVA', 'BBWI', 'BBY', 'BC', 'BCAB', 'BCAL', 'BCC', 'BCE', 'BCH', 'BCLI', 'BCML', 'BCO', 'BCOV', 
'BCPC', 'BCRX', 'BCS', 'BCSF', 'BCYC', 'BDC', 'BDSX', 'BDTX', 'BDX', 'BEAM', 'BEAT', 'BEEM', 'BEKE',
'BEN', 'BERY', 'BFAM', 'BFC','BFH', 'BFIN', 'BFRI', 'BFST', 'BG', 'BGNE', 'BGS', 'BGSF', 'BHC', 'BHE', 
'BHF', 'BHIL', 'BHP', 'BHR', 'BIDU', 'BIG', 'BIIB', 'BILI', 'BILL', 'BIOR', 'BIP', 'BITF', 'BJRI', 'BKD',
'BKH', 'BKNG', 'BKU', 'BL', 'BLBX', 'BLD', 'BLDP', 'BLDR', 'BLFS', 'BLFY', 'BLK', 'BLKB', 'BLMN',
'BLNK', 'BLRX', 'BLTE', 'BMI', 'BMRC', 'BMRN', 'BMY', 'BNED', 'BNGO','BNL', 'BNOX', 'BNR', 'BNS', 'BNTC',
'BNTX', 'BOH', 'BOKF', 'BOLT', 'BOOM', 'BOOT', 'BORR', 'BPMC', 'BPOP', 'BPRN', 'BPTH', 'BR',
'BRAG', 'BRBR', 'BRFH', 'BRFS', 'BRKR', 'BRO', 'BRO', 'BRT', 'BRTX', 'BRX', 'BRY', 'BSAC',
'BSBR', 'BSET', 'BSIG', 'BSM', 'BSRR', 'BSVN', 'BSX', 'BTAI', 'BTBT', 'BTCS',
'BTI', 'BTOG', 'BTU', 'BUSE', 'BV', 'BVN', 'BWA', 'BWAY', 'BWB', 'BWEN', 'BWFG',
'BWMN', 'BWXT', 'BX', 'BXC', 'BXP', 'BY', 'BYD', 'BYND', 'BYRN', 'BYSI', 'BZH',
'C', 'CAAP', 'CABA', 'CABO', 'CAC', 'CACC', 'CACI', 'CADL', 'CAE', 'CAG', 'CAH',
'CAKE', 'CAL', 'CALM', 'CALT', 'CALX', 'CAMT', 'CAN', 'CAPR', 'CAR', 'CARA',
'CARE', 'CARM', 'CARR', 'CARS', 'CASH', 'CASI', 'CASS', 'CASY', 'CAT', 'CB', 'CBAN',
'CBFV', 'CBNK', 'CBRL', 'CBSH', 'CBT', 'CBU', 'CBZ', 'CC', 'CCB', 'CCBG', 
'CCCC', 'CCCS', 'CCEP', 'CCI', 'CCJ', 'CCK', 'CCL', 'CCLD', 'CCM', 'CCNE',
'CCO', 'CCOI', 'CCRN', 'CCS', 'CCSI', 'CCU', 'CDE', 'CDIO', 'CDLX', 'CDMO', 'CDNA',
'CDNS', 'CDRE', 'CDTX', 'CDXC', 'CDZI','CECO', 'CEG', 'CEIX', 'CELC', 'CELH', 
'CELZ', 'CENT', 'CENX', 'CERS', 'CERT', 'CEVA', 'CF', 'CFB', 'CFFN', 'CFG',
'CFR', 'CG', 'CGAU', 'CGBD', 'CGC', 'CGEM', 'CGEN', 'CGNT', 'CGNX', 'CGTX', 
'CHCT', 'CHCO', 'CHD', 'CHDN', 'CHE', 'CHEF', 'CHGG', 'CHH', 'CHKP', 'CHMG', 
'CHMI', 'CHNR', 'CHRS', 'CHRW', 'CHUY', 'CHX', 'CI', 'CIB', 'CIEN', 'CIFR',
'CIG', 'CIGI', 'CIM', 'CNF', 'CING', 'CIO', 'CION', 'CISO', 'CIVB', 'CIVI',
'CJJD', 'CKPT', 'CL', 'CLAR', 'CLB', 'CLBK', 'CLBT', 'CLDX', 'CLF', 'CLFD',
'CLH', 'CLS', 'CLSD', 'CLSK', 'CLVT', 'CLW', 'CLX', 'CM', 'CMA', 'CMBM',
'CMC', 'CMCO', 'CMG', 'CMI', 'CMMB', 'CMPR', 'CMPS', 'CMPX', 'CMRE', 'CMRX',
'CMS','CMTG', 'CMTL', 'CNA', 'CNC', 'CNDT', 'CNI','CNK', 'CNMD', 'CNNE', 
'CNO', 'CNOB', 'CNP', 'CNQ','CNS', 'CNSL', 'CNTA', 'CNTX', 'CNTY', 'CNX',
'CNXC', 'CNXN', 'COCO', 'COCP', 'CODA', 'CODI', 'CODX', 'COF', 'COGT', 'COHU',
'COLB', 'COLD', 'COLL', 'COLM', 'COO', 'COOK', 'COOP', 'COP', 'CORT', 'COST','COUR',
'COYA', 'CP', 'CPB', 'CPF', 'CPK', 'CPLP','CPRI', 'CPRT', 'CPRX', 'CPS', 'CPTN',
'CRAI', 'CRBP', 'CRBU','CRGO', 'CRH' ,'CRI' ,'CRIS', 'CRK', 'CRL' ,'CRM', 'CRMD', 'CRMT' ,'CRNC', 'CRNT', 'CRNX',
'CRON', 'CROX' ,'CRS' ,'CRSR' ,'CRTO', 'CRUS', 'CRVS', 'CSAN' ,'CSBR', 'CSCO', 'CSGP', 'CSGS', 
'CSIQ', 'CSL', 'CSR', 'CSTE' ,'CSTL',  'CSV' ,'CSWC' ,'CSWI', 'CSX', 'CTAS', 'CTBI', 'CTLP', 'CTLT' ,
'CTMX','CTRA', 'CTRE' ,'CTRN', 'CTS','CTSO', 'CTV' ,'CTVA', 'CTXR','CUBE', 'CUE' , 'CULP', 'CURV' ,
'CUTR', 'CUZ', 'CVAC', 'CVBF', 'CVCO', 'CVE',  'CVEO', 'CVGI', 'CVGW', 'CVI', 'CVLT', 'CVRX', 'CVS',
 'CVX', 'CW', 'CWBC', 'CWCO', 'CWK' ,'CWT' ,'CXDO', 'CXW', 'CYBR', 'CYCC', 'CYH', 'CYN', 'CYRX', 
'CYTK', 'CYTO' ,'CZNC', 'CZR' ,'D', 'DAC', 'DADA' ,'DAIO' , 'DAL', 'DAN', 'DAO', 'DAR', 'DARE' ,'DAVA',
'DAWN',  'DB', 'DBVT', 'DCBO', 'DCGO', 'DCI', 'DCO', 'DCOM', 'DCTH', 'DD','DDD','DDI', 'DE', 'DEA', 'DECK',
'DEI', 'DELL', 'DENN', 'DEO', 'DERM','DESP', 'DFIN', 'DFLI', 'DFS', 'DGII','DGX', 'DHC', 'DHI', 'DHR',
'DHT', 'DHX','DIBS', 'DIN', 'DINO', 'DIOD', 'DIS', 'DK', 'DKL', 'DLHC', 'DLNG', 'DLO', 'DLPN', 'DLR', 'DLX']


    
    filename = f'resultats.csv'
    for action in univers:
        for earning in earnings:
            try:
                await extraction(filename, earning, action, combinaison) 
                
            except ValueError as e:
                # Log l'erreur pour savoir quelles actions ont posé problème
                print(f"Erreur pour l'action {action}: {e}")
                # Passer à l'action suivante
                continue
            except Exception as e:
                # Gestion des autres types d'erreurs si nécessaire
                print(f"Erreur inattendue pour l'action {action}: {e}")
                continue
         
        

# Exécutez la fonction principale
asyncio.run(main()) 
