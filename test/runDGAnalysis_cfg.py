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
    input = cms.untracked.int32(50000)
)



process.source = cms.Source(
    "PoolSource",
    fileNames = cms.untracked.vstring(
       'file:/eos/user/f/fernance/LLPNTuples/Central/modifiedDY/EXO-RunIISummer16MiniAODv3-08121_320.root',       
       'file:/eos/user/f/fernance/LLPNTuples/Central/modifiedDY/EXO-RunIISummer16MiniAODv3-08121_321.root',       
       'file:/eos/user/f/fernance/LLPNTuples/Central/modifiedDY/EXO-RunIISummer16MiniAODv3-08121_322.root',       
       'file:/eos/user/f/fernance/LLPNTuples/Central/modifiedDY/EXO-RunIISummer16MiniAODv3-08121_324.root',       
       'file:/eos/user/f/fernance/LLPNTuples/Central/modifiedDY/EXO-RunIISummer16MiniAODv3-08121_325.root',       
       'file:/eos/user/f/fernance/LLPNTuples/Central/modifiedDY/EXO-RunIISummer16MiniAODv3-08121_326.root',       
       'file:/eos/user/f/fernance/LLPNTuples/Central/modifiedDY/EXO-RunIISummer16MiniAODv3-08121_327.root',       
       'file:/eos/user/f/fernance/LLPNTuples/Central/modifiedDY/EXO-RunIISummer16MiniAODv3-08121_328.root',       
       'file:/eos/user/f/fernance/LLPNTuples/Central/modifiedDY/EXO-RunIISummer16MiniAODv3-08121_329.root',       
       'file:/eos/user/f/fernance/LLPNTuples/Central/modifiedDY/EXO-RunIISummer16MiniAODv3-08121_987.root',       
       'file:/eos/user/f/fernance/LLPNTuples/Central/modifiedDY/EXO-RunIISummer16MiniAODv3-08121_1000.root',       
       'file:/eos/user/f/fernance/LLPNTuples/Central/modifiedDY/EXO-RunIISummer16MiniAODv3-08121_1001.root',       
       'file:/eos/user/f/fernance/LLPNTuples/Central/modifiedDY/EXO-RunIISummer16MiniAODv3-08121_1002.root',       
       'file:/eos/user/f/fernance/LLPNTuples/Central/modifiedDY/EXO-RunIISummer16MiniAODv3-08121_1003.root',       
       'file:/eos/user/f/fernance/LLPNTuples/Central/modifiedDY/EXO-RunIISummer16MiniAODv3-08121_1004.root'       
    )
)



## path definitions
process.p      = cms.Path(
    process.DGAnalysis

)

