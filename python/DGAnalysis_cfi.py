import FWCore.ParameterSet.Config as cms

DGAnalysis = cms.EDAnalyzer('DGAnalysis',
    nameOfOutput = cms.string('output.root'),
    EventInfo = cms.InputTag("generator"),
    RunInfo = cms.InputTag("generator"),
    BeamSpot = cms.InputTag("offlineBeamSpot"),
    GenParticleCollection = cms.InputTag("genParticles"),
    GlobalMuonCollection = cms.InputTag("globalMuons"),
    DisplacedGlobalCollection = cms.InputTag("displacedGlobalMuons"),
    theGenEventInfoProduct = cms.InputTag("generator"),
)


