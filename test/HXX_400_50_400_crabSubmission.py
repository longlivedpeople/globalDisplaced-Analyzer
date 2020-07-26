from WMCore.Configuration import Configuration
config = Configuration()

config.section_('General')
config.General.transferLogs = True
config.General.requestName = 'HXX_400_50_400_DGNTuple'
config.General.instance = 'prod'

config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'runDGAnalysis_cfg.py'
config.JobType.disableAutomaticOutputCollection = True
config.JobType.outputFiles = ['DGNTuple.root']
config.JobType.maxMemoryMB = 2500

config.section_('Data')
config.Data.inputDBS = 'phys03'
#config.Data.unitsPerJob = 1
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 10
#config.Data.totalUnits = 50
config.Data.inputDataset = '/H2ToLLPXToLeptons_MH_400_MX_50_ctau_400mm_TuneCP2_13TeV_pythia8_80X_13082019-1313/fernance-400-50-400_HXX_RunIISummer16MiniAODv3_230220-1650-bd3e7bcff6c9bcad356ea4ed7e4f08b4/USER'
config.Data.publication = False
config.Data.outLFNDirBase = '/store/user/fernance/' 

config.section_('Site')
config.Site.storageSite = 'T2_ES_IFCA'
