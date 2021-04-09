#include "Analysis/globalDisplaced-Analyzer/src/DGAnalysis.h"

////////
//////// -- Constructor
////////
DGAnalysis::DGAnalysis(const edm::ParameterSet& iConfig)
{
   usesResource("TFileService");

   parameters = iConfig;

   TriggerBitsToken_ = consumes<edm::TriggerResults> (parameters.getParameter<edm::InputTag>("bits"));
   PUSummaryToken_ = consumes<std::vector<PileupSummaryInfo> > (parameters.getParameter<edm::InputTag>("PileUpSummary"));
   PVToken_ = consumes<edm::View<reco::Vertex> > (parameters.getParameter<edm::InputTag>("PVCollection"));
   GenParticleToken_ = consumes<edm::View<reco::GenParticle> >  (parameters.getParameter<edm::InputTag>("GenParticleCollection"));
   TrackToken_ = consumes<edm::View<reco::Track> >  (parameters.getParameter<edm::InputTag>("TrackCollection"));
   DisplacedGlobalToken_ = consumes<edm::View<reco::Track> >  (parameters.getParameter<edm::InputTag>("DisplacedGlobalCollection"));
   DisplacedStandaloneToken_ = consumes<edm::View<reco::Track> >  (parameters.getParameter<edm::InputTag>("DisplacedStandaloneCollection"));
   GlobalMuonToken_ = consumes<edm::View<reco::Track> >  (parameters.getParameter<edm::InputTag>("GlobalMuonCollection"));
   JetToken_ = consumes<edm::View<pat::Jet> >  (parameters.getParameter<edm::InputTag>("JetCollection"));
   GenJetToken_ = consumes<edm::View<reco::GenJet> >  (parameters.getParameter<edm::InputTag>("GenJetCollection"));

}



////////
//////// -- Destructor
////////
DGAnalysis::~DGAnalysis()
{

}

////////
//////// -- BeginJob
////////
void DGAnalysis::beginJob()
{
  std::cout << "Begin Job" << std::endl;

  output_filename = parameters.getParameter<std::string>("nameOfOutput");
  file_out = new TFile(output_filename.c_str(), "RECREATE");

  tree_out = new TTree("Events", "Events"); // declaration

  //
  // -- Set the output TTree branches
  //
  
  tree_out->Branch("eventId", &eventId, "eventId/I");
  tree_out->Branch("luminosityBlock", &luminosityBlock, "luminosityBlock/I");
  tree_out->Branch("run", &run, "run/I");

  tree_out->Branch("Flag_HLT_IsoMu24", &Flag_HLT_IsoMu24, "Flag_HLT_IsoMu24/O");

  tree_out->Branch("nPU", &nPU, "nPU/I");
  tree_out->Branch("nPUTrue", &nPUTrue, "nPUTrue/I");

  tree_out->Branch("PV_vx", &PV_vx, "PV_vx/F");
  tree_out->Branch("PV_vy", &PV_vy, "PV_vy/F");
  tree_out->Branch("PV_vz", &PV_vz, "PV_vz/F");

  tree_out->Branch("ngenMu", &ngenMu, "ngenMu/I");
  tree_out->Branch("genMu_pt", genMu_pt, "genMu_pt[ngenMu]/F");
  tree_out->Branch("genMu_eta", genMu_eta, "genMu_eta[ngenMu]/F");
  tree_out->Branch("genMu_phi", genMu_phi, "genMu_phi[ngenMu]/F");
  tree_out->Branch("genMu_dxy", genMu_dxy, "genMu_dxy[ngenMu]/F");
  tree_out->Branch("genMu_dxy0", genMu_dxy0, "genMu_dxy0[ngenMu]/F");
  tree_out->Branch("genMu_dz", genMu_dz, "genMu_dz[ngenMu]/F");
  tree_out->Branch("genMu_dz0", genMu_dz0, "genMu_dz0[ngenMu]/F");
  tree_out->Branch("genMu_vx", genMu_vx, "genMu_vx[ngenMu]/F");
  tree_out->Branch("genMu_vy", genMu_vy, "genMu_vy[ngenMu]/F");
  tree_out->Branch("genMu_vz", genMu_vz, "genMu_vz[ngenMu]/F");
  tree_out->Branch("genMu_pdgId", genMu_pdgId, "genMu_pdgId[ngenMu]/I");
  tree_out->Branch("genMu_motherPdgId", genMu_motherPdgId, "genMu_motherPdgId[ngenMu]/I");
  tree_out->Branch("genMu_isPromptFinalState", genMu_isPromptFinalState, "genMu_isPromptFinalState[ngenMu]/I");
  tree_out->Branch("genMu_isDirectPromptTauDecayProductFinalState", genMu_isDirectPromptTauDecayProductFinalState, "genMu_isDirectPromptTauDecayProductFinalState[ngenMu]/I");
  tree_out->Branch("genMu_isDirectHadronDecayProduct", genMu_isDirectHadronDecayProduct, "genMu_isDirectHadronDecayProduct[ngenMu]/I");
  
  tree_out->Branch("nGM", &nGM, "nGM/I");
  tree_out->Branch("GM_pt", GM_pt, "GM_pt[nGM]/F");
  tree_out->Branch("GM_ptError", GM_ptError, "GM_ptError[nGM]/F");
  tree_out->Branch("GM_eta", GM_eta, "GM_eta[nGM]/F");
  tree_out->Branch("GM_phi", GM_phi, "GM_phi[nGM]/F");
  tree_out->Branch("GM_vx", GM_vx, "GM_vx[nGM]/F");
  tree_out->Branch("GM_vy", GM_vy, "GM_vy[nGM]/F");
  tree_out->Branch("GM_vz", GM_vz, "GM_vz[nGM]/F");
  tree_out->Branch("GM_dxy", GM_dxy, "GM_dxy[nGM]/F");
  tree_out->Branch("GM_dxyError", GM_dxyError, "GM_dxyError[nGM]/F");
  tree_out->Branch("GM_dxy0", GM_dxy0, "GM_dxy0[nGM]/F");
  tree_out->Branch("GM_dxy0Error", GM_dxy0Error, "GM_dxy0Error[nGM]/F");
  tree_out->Branch("GM_Ixy", GM_Ixy, "GM_Ixy[nGM]/F");
  tree_out->Branch("GM_dz", GM_dz, "GM_dz[nGM]/F");
  tree_out->Branch("GM_dzError", GM_dzError, "GM_dzError[nGM]/F");
  tree_out->Branch("GM_dz0", GM_dz0, "GM_dz0[nGM]/F");
  tree_out->Branch("GM_dz0Error", GM_dz0Error, "GM_dz0Error[nGM]/F");
  tree_out->Branch("GM_Iz", GM_Iz, "GM_Iz[nGM]/F");
  tree_out->Branch("GM_q", GM_q, "GM_q[nGM]/I");
  tree_out->Branch("GM_numberOfValidHits", GM_numberOfValidHits, "GM_numberOfValidHits[nGM]/I");
  tree_out->Branch("GM_numberOfLostHits", GM_numberOfLostHits, "GM_numberOfLostHits[nGM]/I");
  tree_out->Branch("GM_chi2", GM_chi2, "GM_chi2[nGM]/F");
  tree_out->Branch("GM_ndof", GM_ndof, "GM_ndof[nGM]/F");
  tree_out->Branch("GM_normChi2", GM_normChi2, "GM_normChi2[nGM]/F");

  tree_out->Branch("nDG", &nDG, "nDG/I");
  tree_out->Branch("DG_pt", DG_pt, "DG_pt[nDG]/F");
  tree_out->Branch("DG_ptError", DG_ptError, "DG_ptError[nDG]/F");
  tree_out->Branch("DG_eta", DG_eta, "DG_eta[nDG]/F");
  tree_out->Branch("DG_phi", DG_phi, "DG_phi[nDG]/F");
  tree_out->Branch("DG_vx", DG_vx, "DG_vx[nDG]/F");
  tree_out->Branch("DG_vy", DG_vy, "DG_vy[nDG]/F");
  tree_out->Branch("DG_vz", DG_vz, "DG_vz[nDG]/F");
  tree_out->Branch("DG_dxy", DG_dxy, "DG_dxy[nDG]/F");
  tree_out->Branch("DG_dxyError", DG_dxyError, "DG_dxyError[nDG]/F");
  tree_out->Branch("DG_dxy0", DG_dxy0, "DG_dxy0[nDG]/F");
  tree_out->Branch("DG_dxy0Error", DG_dxy0Error, "DG_dxy0Error[nDG]/F");
  tree_out->Branch("DG_Ixy", DG_Ixy, "DG_Ixy[nDG]/F");
  tree_out->Branch("DG_dz", DG_dz, "DG_dz[nDG]/F");
  tree_out->Branch("DG_dzError", DG_dzError, "DG_dzError[nDG]/F");
  tree_out->Branch("DG_dz0", DG_dz0, "DG_dz0[nDG]/F");
  tree_out->Branch("DG_dz0Error", DG_dz0Error, "DG_dz0Error[nDG]/F");
  tree_out->Branch("DG_Iz", DG_Iz, "DG_Iz[nDG]/F");
  tree_out->Branch("DG_q", DG_q, "DG_q[nDG]/I");
  tree_out->Branch("DG_numberOfValidHits", DG_numberOfValidHits, "DG_numberOfValidHits[nDG]/I");
  tree_out->Branch("DG_numberOfLostHits", DG_numberOfLostHits, "DG_numberOfLostHits[nDG]/I");
  tree_out->Branch("DG_chi2", DG_chi2, "DG_chi2[nDG]/F");
  tree_out->Branch("DG_ndof", DG_ndof, "DG_ndof[nDG]/F");
  tree_out->Branch("DG_normChi2", DG_normChi2, "DG_normChi2[nDG]/F");
  tree_out->Branch("DG_nPB", DG_nPB, "DG_nPB[nDG]/I");
  tree_out->Branch("DG_nPE", DG_nPE, "DG_nPE[nDG]/I");
  tree_out->Branch("DG_nTIB", DG_nTIB, "DG_nTIB[nDG]/I");
  tree_out->Branch("DG_nTOB", DG_nTOB, "DG_nTOB[nDG]/I");
  tree_out->Branch("DG_nTID", DG_nTID, "DG_nTID[nDG]/I");
  tree_out->Branch("DG_nTEC", DG_nTEC, "DG_nTEC[nDG]/I");
  tree_out->Branch("DG_nDT", DG_nDT, "DG_nDT[nDG]/I");
  tree_out->Branch("DG_nCSC", DG_nCSC, "DG_nCSC[nDG]/I");
  tree_out->Branch("DG_nRPC", DG_nRPC, "DG_nRPC[nDG]/I");
  tree_out->Branch("DG_nGEM", DG_nGEM, "DG_nGEM[nDG]/I");
  tree_out->Branch("DG_nME0", DG_nME0, "DG_nME0[nDG]/I");
  tree_out->Branch("DG_muonStations", DG_muonStations, "DG_muonStations[nDG]/I");
  tree_out->Branch("DG_muonHits", DG_muonHits, "DG_muonHits[nDG]/I");
  tree_out->Branch("DG_outerTrackerHits", DG_outerTrackerHits, "DG_outerTrackerHits[nDG]/I");
  tree_out->Branch("DG_totalHits", DG_totalHits, "DG_totalHits[nDG]/I");
  tree_out->Branch("DG_DTHits", DG_DTHits, "DG_DTHits[nDG]/I");
  tree_out->Branch("DG_CSCHits", DG_CSCHits, "DG_CSCHits[nDG]/I");


  tree_out->Branch("nDSA", &nDSA, "nDSA/I");
  tree_out->Branch("DSA_pt", DSA_pt, "DSA_pt[nDSA]/F");
  tree_out->Branch("DSA_ptError", DSA_ptError, "DSA_ptError[nDSA]/F");
  tree_out->Branch("DSA_eta", DSA_eta, "DSA_eta[nDSA]/F");
  tree_out->Branch("DSA_phi", DSA_phi, "DSA_phi[nDSA]/F");
  tree_out->Branch("DSA_vx", DSA_vx, "DSA_vx[nDSA]/F");
  tree_out->Branch("DSA_vy", DSA_vy, "DSA_vy[nDSA]/F");
  tree_out->Branch("DSA_vz", DSA_vz, "DSA_vz[nDSA]/F");
  tree_out->Branch("DSA_dxy", DSA_dxy, "DSA_dxy[nDSA]/F");
  tree_out->Branch("DSA_dxyError", DSA_dxyError, "DSA_dxyError[nDSA]/F");
  tree_out->Branch("DSA_dxy0", DSA_dxy0, "DSA_dxy0[nDSA]/F");
  tree_out->Branch("DSA_dxy0Error", DSA_dxy0Error, "DSA_dxy0Error[nDSA]/F");
  tree_out->Branch("DSA_Ixy", DSA_Ixy, "DSA_Ixy[nDSA]/F");
  tree_out->Branch("DSA_dz", DSA_dz, "DSA_dz[nDSA]/F");
  tree_out->Branch("DSA_dzError", DSA_dzError, "DSA_dzError[nDSA]/F");
  tree_out->Branch("DSA_dz0", DSA_dz0, "DSA_dz0[nDSA]/F");
  tree_out->Branch("DSA_dz0Error", DSA_dz0Error, "DSA_dz0Error[nDSA]/F");
  tree_out->Branch("DSA_Iz", DSA_Iz, "DSA_Iz[nDSA]/F");
  tree_out->Branch("DSA_q", DSA_q, "DSA_q[nDSA]/I");
  tree_out->Branch("DSA_numberOfValidHits", DSA_numberOfValidHits, "DSA_numberOfValidHits[nDSA]/I");
  tree_out->Branch("DSA_numberOfLostHits", DSA_numberOfLostHits, "DSA_numberOfLostHits[nDSA]/I");
  tree_out->Branch("DSA_chi2", DSA_chi2, "DSA_chi2[nDSA]/F");
  tree_out->Branch("DSA_ndof", DSA_ndof, "DSA_ndof[nDSA]/F");
  tree_out->Branch("DSA_normChi2", DSA_normChi2, "DSA_normChi2[nDSA]/F");


  tree_out->Branch("nJet", &nJet, "nJet/I");
  tree_out->Branch("Jet_pt", Jet_pt, "Jet_pt[nJet]/F");
  tree_out->Branch("Jet_eta", Jet_eta, "Jet_eta[nJet]/F");
  tree_out->Branch("Jet_phi", Jet_phi, "Jet_phi[nJet]/F");

  tree_out->Branch("nGenJet", &nGenJet, "nGenJet/I");
  tree_out->Branch("GenJet_pt", GenJet_pt, "GenJet_pt[nGenJet]/F");
  tree_out->Branch("GenJet_eta", GenJet_eta, "GenJet_eta[nGenJet]/F");
  tree_out->Branch("GenJet_phi", GenJet_phi, "GenJet_phi[nGenJet]/F");

}

////////
//////// -- EndJob
////////
void DGAnalysis::endJob()
{
  std::cout << "End Job" << std::endl;

  file_out->cd();
  tree_out->Write();
  file_out->Close();

}


////////
//////// -- fillDescriptions
////////
void DGAnalysis::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}


////////
//////// -- Analyze
////////
void DGAnalysis::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{

   bool ValidTriggerBits = iEvent.getByToken(TriggerBitsToken_, triggerBits_);

   bool ValidPUSummary = iEvent.getByToken(PUSummaryToken_, puInfoH_);

   bool ValidPV = iEvent.getByToken(PVToken_, PVCollection_);

   bool ValidGenParticles = iEvent.getByToken(GenParticleToken_, GenParticleCollection_);
   if (!ValidGenParticles) { return; }

   bool ValidTracks = iEvent.getByToken(TrackToken_, TrackCollection_);

   bool ValidDisplacedGlobal = iEvent.getByToken(DisplacedGlobalToken_, DisplacedGlobalCollection_);
   if (!ValidDisplacedGlobal) { return; }

   bool ValidDisplacedStandalone = iEvent.getByToken(DisplacedStandaloneToken_, DisplacedStandaloneCollection_);
   if (!ValidDisplacedStandalone) { return; }

   bool ValidGlobalMuon = iEvent.getByToken(GlobalMuonToken_, GlobalMuonCollection_);
   if (!ValidGlobalMuon) { return; }

   bool ValidJet = iEvent.getByToken(JetToken_, JetCollection_);
   //if (!ValidJet) { return; }

   bool ValidGenJet = iEvent.getByToken(GenJetToken_, GenJetCollection_);
   //if (!ValidGenJet) { return; }

   iSetup.get<TransientTrackRecord>().get("TransientTrackBuilder",TransientTrackBuilder_);


   //
   // -- Init the variables
   //    Class variables values are kept from one event to the next so it is
   //    necessary to set all values to zero before moving
   //

   // -> Event info
   eventId = 0;
   luminosityBlock = 0;
   run = 0;

   // -> HLT
   Flag_HLT_IsoMu24 = false;


   // -> Pileup
   nPU = 0;
   nPUTrue = 0;

   // -> Primary vertex
   PV_vx = 0.;
   PV_vy = 0.;
   PV_vz = 0.;

   // -> Generated muons   
   for (Int_t i = 0; i < ngenMu; i++) {

     genMu_pt[i] = 0.;
     genMu_eta[i] = 0.;
     genMu_phi[i] = 0.;
     genMu_dxy[i] = 0.;
     genMu_dz[i] = 0.;
     genMu_dxy0[i] = 0.;
     genMu_dz0[i] = 0.;
     genMu_vx[i] = 0.;
     genMu_vy[i] = 0.;
     genMu_vz[i] = 0.;
     genMu_pdgId[i] = 0;
     genMu_motherPdgId[i] = 0;
     genMu_isPromptFinalState[i] = 0;
     genMu_isDirectPromptTauDecayProductFinalState[i] = 0;
     genMu_isDirectHadronDecayProduct[i] = 0;

   }
   ngenMu = 0;

   // -> Global muons
   for (Int_t i = 0; i < nGM; i++) {

     GM_pt[i] = 0.;
     GM_ptError[i] = 0.;
     GM_eta[i] = 0.;
     GM_phi[i] = 0.;
     GM_vx[i] = 0.;
     GM_vy[i] = 0.;
     GM_vz[i] = 0.;
     GM_dxy[i] = 0.;
     GM_dxyError[i] = 0.;
     GM_dxy0[i] = 0.;
     GM_dxy0Error[i] = 0.;
     GM_Ixy[i] = 0.;
     GM_dz[i] = 0.;
     GM_dzError[i] = 0.;
     GM_dz0[i] = 0.;
     GM_dz0Error[i] = 0.;
     GM_Iz[i] = 0.;
     GM_q[i] = 0;
     GM_numberOfValidHits[i] = 0;
     GM_numberOfLostHits[i] = 0;
     GM_chi2[i] = 0.;
     GM_ndof[i] = 0.;
     GM_normChi2[i] = 0.;
   }
   nGM = 0;

   // -> Displaced global
   for (Int_t i = 0; i < nDG; i++) {

     DG_pt[i] = 0.;
     DG_ptError[i] = 0.;
     DG_eta[i] = 0.;
     DG_phi[i] = 0.;
     DG_vx[i] = 0.;
     DG_vy[i] = 0.;
     DG_vz[i] = 0.;
     DG_dxy[i] = 0.;
     DG_dxyError[i] = 0.;
     DG_dxy0[i] = 0.;
     DG_dxy0Error[i] = 0.;
     DG_Ixy[i] = 0.;
     DG_dz[i] = 0.;
     DG_dzError[i] = 0.;
     DG_dz0[i] = 0.;
     DG_dz0Error[i] = 0.;
     DG_Iz[i] = 0.;
     DG_q[i] = 0;
     DG_numberOfValidHits[i] = 0;
     DG_numberOfLostHits[i] = 0;
     DG_chi2[i] = 0.;
     DG_ndof[i] = 0.;
     DG_normChi2[i] = 0.;
     DG_nPB[i] = 0;
     DG_nPE[i] = 0;
     DG_nTIB[i] = 0;
     DG_nTOB[i] = 0;
     DG_nTID[i] = 0;
     DG_nTEC[i] = 0;
     DG_nDT[i] = 0;
     DG_nCSC[i] = 0;
     DG_nRPC[i] = 0;
     DG_nGEM[i] = 0;
     DG_nME0[i] = 0;
     DG_muonStations[i] = 0;
     DG_muonHits[i] = 0;
     DG_outerTrackerHits[i] = 0;
     DG_trackerHits[i] = 0;
     DG_totalHits[i] = 0;
     DG_DTHits[i] = 0;
     DG_CSCHits[i] = 0;
   }
   nDG = 0;
   
   // -> Displaced standalone
   for (Int_t i = 0; i < nDSA; i++) {

     DSA_pt[i] = 0.;
     DSA_ptError[i] = 0.;
     DSA_eta[i] = 0.;
     DSA_phi[i] = 0.;
     DSA_vx[i] = 0.;
     DSA_vy[i] = 0.;
     DSA_vz[i] = 0.;
     DSA_dxy[i] = 0.;
     DSA_dxyError[i] = 0.;
     DSA_dxy0[i] = 0.;
     DSA_dxy0Error[i] = 0.;
     DSA_Ixy[i] = 0.;
     DSA_dz[i] = 0.;
     DSA_dzError[i] = 0.;
     DSA_dz0[i] = 0.;
     DSA_dz0Error[i] = 0.;
     DSA_Iz[i] = 0.;
     DSA_q[i] = 0;
     DSA_numberOfValidHits[i] = 0;
     DSA_numberOfLostHits[i] = 0;
     DSA_chi2[i] = 0.;
     DSA_ndof[i] = 0.;
     DSA_normChi2[i] = 0.;
   }
   nDSA = 0;


   // -> Jets
   for (Int_t i = 0; i < nJet; i++) {

     Jet_pt[i] = 0.;
     Jet_eta[i] = 0.;
     Jet_phi[i] = 0.;

   }
   nJet = 0;


   // -> GenJets
   for (Int_t i = 0; i < nGenJet; i++) {

     GenJet_pt[i] = 0.;
     GenJet_eta[i] = 0.;
     GenJet_phi[i] = 0.;

   }
   nGenJet = 0;




   //
   // -- Pre-analysis
   //

   // -> Event info
   eventId = iEvent.id().event();
   luminosityBlock = iEvent.id().luminosityBlock();
   run = iEvent.id().run();


   // -> Primary vertex
   const reco::Vertex &thePV = (*PVCollection_)[0];
   PV_vx = thePV.x();
   PV_vy = thePV.y();
   PV_vz = thePV.z();

   // -> Pile up
   for (size_t i = 0; i < puInfoH_->size(); i++){
      if (puInfoH_->at(i).getBunchCrossing() == 0) {
         nPU = puInfoH_->at(i).getPU_NumInteractions();
         nPUTrue = puInfoH_->at(i).getTrueNumInteractions();
         continue;
      }
   }


   //
   // -- HLT analysis
   //
   const edm::TriggerNames &names = iEvent.triggerNames(*triggerBits_); 
   Flag_HLT_IsoMu24 = triggerBits_->accept(names.triggerIndex(getPathVersion(names, "HLT_IsoMu24_v")));


   //
   // -- Main analysis
   //


   // -> MC truth:
   analyzeGenParticles(iEvent);

   std::cout << ">> Tracks: " << std::endl;
   if (ValidTracks) analyzeTracks(iEvent);
   std::cout << "\n" << std::endl;

   // -> Muon analysis:
   std::cout << ">> DisplacedGlobals: " << std::endl;
   analyzeDisplacedGlobal(iEvent);
   analyzeDisplacedStandalone(iEvent);
   analyzeGlobalMuons(iEvent);
   analyzeJets(iEvent);
   analyzeGenJets(iEvent);

   if (ngenMu < 1 && nDG < 1 && nGM < 1) {return;}

   // -> Fill the TTree

   tree_out->Fill();

}


void DGAnalysis::analyzeGenParticles(const edm::Event& iEvent)
{

   // if (isData): return; -> To be implemented
   std::vector<int> iGL; // Now truncated to muons

   reco::GenParticleRef mref;
   reco::GenParticle m;

   // Find status 1 muons:
   for (size_t i = 0; i < GenParticleCollection_->size(); i++){

      const reco::GenParticle &gp = (*GenParticleCollection_)[i];
      if (abs(gp.pdgId()) == 13 && gp.status() == 1) {  iGL.push_back(i);  }

   }

   // Process status 1 muons:
   ngenMu = iGL.size();
   std::sort( std::begin(iGL), std::end(iGL), [&](int i1, int i2){ return GenParticleCollection_->at(i1).pt() > GenParticleCollection_->at(i2).pt(); });

   for (size_t i = 0; i < iGL.size(); i++){

      const reco::GenParticle &gp = (*GenParticleCollection_)[iGL.at(i)];

      genMu_pt[i] = gp.pt();
      genMu_eta[i] = gp.eta();
      genMu_phi[i] = gp.phi();
      genMu_pdgId[i] = gp.pdgId();
      genMu_isPromptFinalState[i] = gp.isPromptFinalState();
      genMu_isDirectPromptTauDecayProductFinalState[i] = gp.isDirectPromptTauDecayProductFinalState();
      genMu_isDirectHadronDecayProduct[i] = gp.statusFlags().isDirectHadronDecayProduct();

      double lambda = 3.14/2. - gp.theta();

      // bottom-up to get the real decaying particle:
      if (gp.mother()->pdgId() == gp.pdgId()) {

         mref = gp.motherRef();
         m = *mref;
         while (m.pdgId() == m.mother()->pdgId()){
            mref = m.motherRef();
            m = *mref;
         }

         genMu_vx[i] = m.vx();
         genMu_vy[i] = m.vy();
         genMu_vz[i] = m.vz();
         genMu_dxy[i] = -(m.vx() - PV_vx)*sin(gp.phi()) + (m.vy() - PV_vy)*cos(gp.phi()); // OJOOOOO
         genMu_dz[i] = 1./cos(lambda)*((m.vz()-PV_vz)*cos(lambda) - ((m.vx() - PV_vx)*cos(gp.phi()) + (m.vy() - PV_vy)*sin(gp.phi()))*sin(lambda)); // OJOOOOO
         genMu_dxy0[i] = -(m.vx())*sin(gp.phi()) + (m.vy())*cos(gp.phi()); // OJOOOOO
         genMu_dz0[i] = 1./cos(lambda)*((m.vz())*cos(lambda) - ((m.vx())*cos(gp.phi()) + (m.vy())*sin(gp.phi()))*sin(lambda)); // OJOOOOO

         if (m.numberOfMothers() != 0){
            genMu_motherPdgId[i] = m.motherRef()->pdgId();
         } else {
            genMu_motherPdgId[i] = 0;
         }

      } else {

         genMu_vx[i] = gp.vx();
         genMu_vy[i] = gp.vy();
         genMu_vz[i] = gp.vz();
         genMu_dxy[i] = -(gp.vx() - PV_vx)*sin(gp.phi()) + (gp.vy() - PV_vy)*cos(gp.phi()); // OJOOOOO
         genMu_dz[i] = 1./cos(lambda)*((gp.vz()-PV_vz)*cos(lambda) - ((gp.vx() - PV_vx)*cos(gp.phi()) + (gp.vy() - PV_vy)*sin(gp.phi()))*sin(lambda)); // OJOOOOO
         genMu_dxy0[i] = -(gp.vx())*sin(gp.phi()) + (gp.vy())*cos(gp.phi()); // OJOOOOO
         genMu_dz0[i] = 1./cos(lambda)*((gp.vz())*cos(lambda) - ((gp.vx())*cos(gp.phi()) + (gp.vy())*sin(gp.phi()))*sin(lambda)); // OJOOOOO
         genMu_motherPdgId[i] = gp.motherRef()->pdgId();

      }
   }


}


void DGAnalysis::analyzeTracks(const edm::Event& iEvent)
{

   for (size_t i = 0; i < TrackCollection_->size(); i++)
   {

      const reco::Track &track = (*TrackCollection_)[i];

      std::cout << "pt: " << track.pt() << " ;  eta: " << track.eta() << " ;  phi: " << track.phi() << std::endl;

   }

}


void DGAnalysis::analyzeDisplacedGlobal(const edm::Event& iEvent)
{

   nDG = 0;

   for (size_t i = 0; i < DisplacedGlobalCollection_->size(); i++)
   {


      const reco::Track &muon = (*DisplacedGlobalCollection_)[i];
      std::cout << "pt: " << muon.pt() << " ;  eta: " << muon.eta() << " ;  phi: " << muon.phi() << std::endl;
      DG_pt[nDG] = muon.pt();
      DG_ptError[nDG] = muon.ptError();
      DG_eta[nDG] = muon.eta();
      DG_phi[nDG] = muon.phi();
      DG_vx[nDG] = muon.vx();
      DG_vy[nDG] = muon.vy();
      DG_vz[nDG] = muon.vz();
      DG_q[nDG] = muon.charge();
      DG_numberOfValidHits[nDG] = muon.numberOfValidHits();
      DG_numberOfLostHits[nDG] = muon.numberOfLostHits();
      DG_chi2[nDG] = muon.chi2();
      DG_ndof[nDG] = muon.ndof();
      DG_normChi2[nDG] = muon.normalizedChi2();
      DG_muonStations[nDG] = muon.hitPattern().muonStationsWithValidHits();
      DG_muonHits[nDG] = muon.hitPattern().numberOfValidMuonHits();
      DG_outerTrackerHits[nDG] = muon.hitPattern().numberOfValidStripHits();
      DG_trackerHits[nDG] = muon.hitPattern().numberOfValidTrackerHits();
      DG_totalHits[nDG] = muon.hitPattern().numberOfValidHits();
      DG_CSCHits[nDG] = muon.hitPattern().numberOfValidMuonCSCHits();
      DG_DTHits[nDG] = muon.hitPattern().numberOfValidMuonDTHits();
    
      TrajectoryStateClosestToPoint traj = computeTrajectory(muon);
      DG_dxy[nDG] = traj.perigeeParameters().transverseImpactParameter();
      DG_dxyError[nDG] = traj.perigeeError().transverseImpactParameterError();
      DG_Ixy[nDG] = fabs(DG_dxy[nDG]/DG_dxyError[nDG]);
      DG_dxy0[nDG] = muon.dxy();
      DG_dxy0Error[nDG] = muon.dxyError();
      DG_dz[nDG] = traj.perigeeParameters().longitudinalImpactParameter();
      DG_dzError[nDG] = traj.perigeeError().longitudinalImpactParameterError();
      DG_dz0[nDG] = muon.dz();
      DG_dz0Error[nDG] = muon.dzError();
      DG_Iz[nDG] = fabs(DG_dz[nDG]/DG_dzError[nDG]);

      // Check the recHits of the track (if available)
      //const reco::HitPattern &hitpat = muon.hitPattern_;
      int nPB = 0;
      int nPE = 0;
      int nTIB = 0;
      int nTOB = 0;
      int nTID = 0;
      int nTEC = 0;
      int nDT = 0;
      int nCSC = 0;
      int nRPC = 0;
      int nGEM = 0;
      int nME0 = 0;

      for (auto hit = muon.recHitsBegin(); hit != muon.recHitsEnd(); hit++)
      {

         DetId idet = (*hit)->geographicalId(); // get the detector
         //std::cout << (idet.subdetId() == MuonSubdetId::DT) << std::endl;
         //std::cout << idet.det() << "\t" << (idet.subdetId()) << "\t" <<(idet.subdetId() == MuonSubdetId::DT) << std::endl;
 
         if (idet.det() == 1){

            if ( idet.subdetId() == 1 ) {nPB++;}
            else if( idet.subdetId() == 2 ) {nPE++;}
            else if( idet.subdetId() == 3 ) {nTIB++;}
            else if( idet.subdetId() == 4 ) {nTOB++;}
            else if( idet.subdetId() == 5 ) {nTID++;}
            else if( idet.subdetId() == 6) {nTEC++;}

         } else if (idet.det() == 2){

            if ( idet.subdetId() == 1 ) {nDT++;}
            else if( idet.subdetId() == 2 ) {nCSC++;}
            else if( idet.subdetId() == 3 ) {nRPC++;}
            else if( idet.subdetId() == 4 ) {nGEM++;}
            else if( idet.subdetId() == 5 ) {nME0++;}

         }

      }

     DG_nPB[nDG] = nPB;
     DG_nPE[nDG] = nPE;
     DG_nTIB[nDG] = nTIB;
     DG_nTOB[nDG] = nTOB;
     DG_nTID[nDG] = nTID;
     DG_nTEC[nDG] = nTEC;
     DG_nDT[nDG] = nDT;
     DG_nCSC[nDG] = nCSC;
     DG_nRPC[nDG] = nRPC;
     DG_nGEM[nDG] = nGEM;
     DG_nME0[nDG] = nME0;


      //std::cout << "Valid: " << muon.found() << muon.numberOfValidHits() << std::endl;
      //std::cout << "Lost: " << muon.lost() << muon.numberOfLostHits() << std::endl;


      nDG++;

   }

}

void DGAnalysis::analyzeGlobalMuons(const edm::Event& iEvent)
{

   nGM = 0;

   for (size_t i = 0; i < GlobalMuonCollection_->size(); i++)
   {

      const reco::Track &muon = (*GlobalMuonCollection_)[i];
      GM_pt[nGM] = muon.pt();
      GM_ptError[nGM] = muon.ptError();
      GM_eta[nGM] = muon.eta();
      GM_phi[nGM] = muon.phi();
      GM_vx[nGM] = muon.vx();
      GM_vy[nGM] = muon.vy();
      GM_vz[nGM] = muon.vz();
      GM_q[nGM] = muon.charge();
      GM_numberOfValidHits[nGM] = muon.numberOfValidHits();
      GM_numberOfLostHits[nGM] = muon.numberOfLostHits();
      GM_chi2[nGM] = muon.chi2();
      GM_ndof[nGM] = muon.ndof();
      GM_normChi2[nGM] = muon.normalizedChi2();

      TrajectoryStateClosestToPoint traj = computeTrajectory(muon);
      GM_dxy[nGM] = traj.perigeeParameters().transverseImpactParameter();
      GM_dxyError[nGM] = traj.perigeeError().transverseImpactParameterError();
      GM_dxy0[nGM] = muon.dxy();
      GM_dxy0Error[nGM] = muon.dxyError();
      GM_Ixy[nGM] = fabs(GM_dxy[nGM]/GM_dxyError[nGM]);
      GM_dz[nGM] = traj.perigeeParameters().longitudinalImpactParameter();
      GM_dzError[nGM] = traj.perigeeError().longitudinalImpactParameterError();
      GM_dz0[nGM] = muon.dz();
      GM_dz0Error[nGM] = muon.dzError();
      GM_Iz[nGM] = fabs(GM_dz[nGM]/GM_dzError[nGM]);
    
      nGM++;

   }

}


void DGAnalysis::analyzeDisplacedStandalone(const edm::Event& iEvent)
{

   nDSA = 0;

   for (size_t i = 0; i < DisplacedStandaloneCollection_->size(); i++)
   {

      const reco::Track &muon = (*DisplacedStandaloneCollection_)[i];
      DSA_pt[nDSA] = muon.pt();
      DSA_ptError[nDSA] = muon.ptError();
      DSA_eta[nDSA] = muon.eta();
      DSA_phi[nDSA] = muon.phi();
      DSA_vx[nDSA] = muon.vx();
      DSA_vy[nDSA] = muon.vy();
      DSA_vz[nDSA] = muon.vz();
      DSA_q[nDSA] = muon.charge();
      DSA_numberOfValidHits[nDSA] = muon.numberOfValidHits();
      DSA_numberOfLostHits[nDSA] = muon.numberOfLostHits();
      DSA_chi2[nDSA] = muon.chi2();
      DSA_ndof[nDSA] = muon.ndof();
      DSA_normChi2[nDSA] = muon.normalizedChi2();
    
      TrajectoryStateClosestToPoint traj = computeTrajectory(muon);
      DSA_dxy[nDSA] = traj.perigeeParameters().transverseImpactParameter();
      DSA_dxyError[nDSA] = traj.perigeeError().transverseImpactParameterError();
      DSA_Ixy[nDSA] = fabs(DSA_dxy[nDSA]/DSA_dxyError[nDSA]);
      DSA_dxy0[nDSA] = muon.dxy();
      DSA_dxy0Error[nDSA] = muon.dxyError();
      DSA_dz[nDSA] = traj.perigeeParameters().longitudinalImpactParameter();
      DSA_dzError[nDSA] = traj.perigeeError().longitudinalImpactParameterError();
      DSA_dz0[nDSA] = muon.dz();
      DSA_dz0Error[nDSA] = muon.dzError();
      DSA_Iz[nDSA] = fabs(DSA_dz[nDSA]/DSA_dzError[nDSA]);

      nDSA++;

   }

}


void DGAnalysis::analyzeJets(const edm::Event& iEvent)
{

   nJet = 0;

   for (size_t i = 0; i < JetCollection_->size(); i++)
   {
      const pat::Jet &jet = (*JetCollection_)[i];
      Jet_pt[nJet] = jet.pt();
      Jet_eta[nJet] = jet.eta();
      Jet_eta[nJet] = jet.phi();
      
      nJet++;
   }
}


void DGAnalysis::analyzeGenJets(const edm::Event& iEvent)
{

   nGenJet = 0;

   for (size_t i = 0; i < GenJetCollection_->size(); i++)
   {
      const reco::GenJet &jet = (*GenJetCollection_)[i];
      GenJet_pt[nGenJet] = jet.pt();
      GenJet_eta[nGenJet] = jet.eta();
      GenJet_eta[nGenJet] = jet.phi();
      
      nGenJet++;
   }
}


TrajectoryStateClosestToPoint DGAnalysis::computeTrajectory(const reco::Track &track)
{

   // Construct the transient track from the reco::Track
   reco::TransientTrack tk = TransientTrackBuilder_->build(track);

   // Determine the point of reference (Set to PV)
   GlobalPoint vert(PV_vx, PV_vy, PV_vz);
   TrajectoryStateClosestToPoint  traj = tk.trajectoryStateClosestToPoint(vert);

   return traj;

}

std::string DGAnalysis::getPathVersion(const edm:: TriggerNames &names, const std::string &rawPath) {

  std::string version;
  std::string finalPath;

  for (int s = 0; s < 20; s++) {

    version = rawPath + std::to_string(s);
    if (names.size() != names.triggerIndex(version)) {
      finalPath = version;
      break;
    }

  }

  return finalPath;

}


