import FWCore.ParameterSet.Config as cms
process = cms.Process("DGAnalysis")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("TrackingTools/TransientTrack/TransientTrackBuilder_cfi")
process.GlobalTag.globaltag = cms.string("94X_mcRun2_asymptotic_v3")

process.load("Analysis.globalDisplaced-Analyzer.DGAnalysis_cfi")

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(100)
)



process.source = cms.Source(
    "PoolSource",
    fileNames = cms.untracked.vstring(
       'file:/eos/user/f/fernance/LLPNTuples/Central/modifiedDY/EXO-RunIISummer16MiniAODv3-08121_320.root'       
    )
)



## path definitions
process.p      = cms.Path(
    process.DGAnalysis

)

