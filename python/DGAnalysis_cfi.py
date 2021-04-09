import FWCore.ParameterSet.Config as cms

DGAnalysis = cms.EDAnalyzer('DGAnalysis',
    nameOfOutput = cms.string('DGNTuple.root'),
    EventInfo = cms.InputTag("generator"),
    RunInfo = cms.InputTag("generator"),
    BeamSpot = cms.InputTag("offlineBeamSpot"),
    bits = cms.InputTag("TriggerResults", "", "HLT"),
    PileUpSummary = cms.InputTag("slimmedAddPileupInfo"),
    PVCollection = cms.InputTag("offlineSlimmedPrimaryVertices"),
    GenParticleCollection = cms.InputTag("prunedGenParticles"),
    JetCollection = cms.InputTag("slimmedJets"),
    GenJetCollection = cms.InputTag("slimmedGenJets"),
    GlobalMuonCollection = cms.InputTag("globalMuons"),
    TrackCollection = cms.InputTag("generalTracks"),
    DisplacedGlobalCollection = cms.InputTag("displacedGlobalMuons"),
    DisplacedStandaloneCollection = cms.InputTag("displacedStandAloneMuons"),
    theGenEventInfoProduct = cms.InputTag("generator"),
)


