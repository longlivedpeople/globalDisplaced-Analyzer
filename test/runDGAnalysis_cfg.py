import FWCore.ParameterSet.Config as cms
process = cms.Process("DGAnalysis")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load('Configuration.Geometry.GeometryRecoDB_cff')
process.load("TrackingTools/TransientTrack/TransientTrackBuilder_cfi")
process.GlobalTag.globaltag = cms.string("94X_mcRun2_asymptotic_v3")

process.load("Analysis.globalDisplaced-Analyzer.DGAnalysis_cfi")

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(50)
)



process.source = cms.Source(
    "PoolSource",
    fileNames = cms.untracked.vstring(
#    'file:/eos/user/f/fernance/LLP_Analysis/miniAOD_extended/DY_test/EXO-RunIISummer16MiniAODv3-08121_325.root')
#    'das://DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM')
    '/store/mc/RunIIAutumn18DRPremix/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/AODSIM/102X_upgrade2018_realistic_v15-v1/00000/00303F79-7EDF-1648-AA56-058F2F50A006.root')
)



## path definitions
process.p      = cms.Path(
    process.DGAnalysis

)

