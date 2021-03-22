from WMCore.Configuration import Configuration
config = Configuration()

config.section_('General')
config.General.transferLogs = True
config.General.requestName = 'DYJetsToLL_M-50_DGNTuple'
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
config.Data.unitsPerJob = 4
#config.Data.totalUnits = 50
config.Data.inputDataset = '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/fernance-DYJetsToLL_M-50_HXX_RunIISummer16MiniAODv3_modified-bd3e7bcff6c9bcad356ea4ed7e4f08b4/USER'
config.Data.publication = False
config.Data.outLFNDirBase = '/store/user/fernance/' 

config.section_('Site')
config.Site.storageSite = 'T2_ES_IFCA'
