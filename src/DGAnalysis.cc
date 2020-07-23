#include "Analysis/globalDisplaced-Analyzer/src/DGAnalysis.h"

////////
//////// -- Constructor
////////
DGAnalysis::DGAnalysis(const edm::ParameterSet& iConfig)
{
   usesResource("TFileService");

   parameters = iConfig;

   GenParticleToken_ = consumes<edm::View<reco::GenParticle> >  (parameters.getParameter<edm::InputTag>("GenParticleCollection"));
   DisplacedGlobalToken_ = consumes<edm::View<reco::Track> >  (parameters.getParameter<edm::InputTag>("DisplacedGlobalCollection"));
   GlobalMuonToken_ = consumes<edm::View<reco::Track> >  (parameters.getParameter<edm::InputTag>("GlobalMuonCollection"));

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
  
  tree_out->Branch("nGM", &nGM, "nGM/I");
  tree_out->Branch("GM_pt", GM_pt, "GM_pt[nGM]/F");
  tree_out->Branch("GM_ptError", GM_ptError, "GM_ptError[nGM]/F");
  tree_out->Branch("GM_eta", GM_eta, "GM_eta[nGM]/F");
  tree_out->Branch("GM_phi", GM_phi, "GM_phi[nGM]/F");
  tree_out->Branch("GM_dxy", GM_dxy, "GM_dxy[nGM]/F");
  tree_out->Branch("GM_dxyError", GM_dxyError, "GM_dxyError[nGM]/F");
  tree_out->Branch("GM_Ixy", GM_Ixy, "GM_Ixy[nGM]/F");
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
  tree_out->Branch("DG_dxy", DG_dxy, "DG_dxy[nDG]/F");
  tree_out->Branch("DG_dxyError", DG_dxyError, "DG_dxyError[nDG]/F");
  tree_out->Branch("DG_Ixy", DG_Ixy, "DG_Ixy[nDG]/F");
  tree_out->Branch("DG_q", DG_q, "DG_q[nDG]/I");
  tree_out->Branch("DG_numberOfValidHits", DG_numberOfValidHits, "DG_numberOfValidHits[nDG]/I");
  tree_out->Branch("DG_numberOfLostHits", DG_numberOfLostHits, "DG_numberOfLostHits[nDG]/I");
  tree_out->Branch("DG_chi2", DG_chi2, "DG_chi2[nDG]/F");
  tree_out->Branch("DG_ndof", DG_ndof, "DG_ndof[nDG]/F");
  tree_out->Branch("DG_normChi2", DG_normChi2, "DG_normChi2[nDG]/F");


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

   bool ValidGenParticles = iEvent.getByToken(GenParticleToken_, GenParticleCollection_);
   if (!ValidGenParticles) { return; }

   bool ValidDisplacedGlobal = iEvent.getByToken(DisplacedGlobalToken_, DisplacedGlobalCollection_);
   if (!ValidDisplacedGlobal) { return; }

   bool ValidGlobalMuon = iEvent.getByToken(GlobalMuonToken_, GlobalMuonCollection_);
   if (!ValidGlobalMuon) { return; }


   std::cout << "Im here" << std::endl;

   //
   // -- Init the variables
   //    Class variables values are kept from one event to the next so it is
   //    necessary to set all values to zero before moving
   //
   
   // -> Global muons
   for (Int_t i = 0; i < nGM; i++) {

     GM_pt[i] = 0.;
     GM_ptError[i] = 0.;
     GM_eta[i] = 0.;
     GM_phi[i] = 0.;
     GM_dxy[i] = 0.;
     GM_dxyError[i] = 0.;
     GM_Ixy[i] = 0.;
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
     DG_dxy[i] = 0.;
     DG_dxyError[i] = 0.;
     DG_Ixy[i] = 0.;
     DG_q[i] = 0;
     DG_numberOfValidHits[i] = 0;
     DG_numberOfLostHits[i] = 0;
     DG_chi2[i] = 0.;
     DG_ndof[i] = 0.;
     DG_normChi2[i] = 0.;
   }
   nDG = 0;
   




   // Analyze functions

   analyzeDisplacedGlobal(iEvent);
   analyzeGlobalMuons(iEvent);


   // Fill the TTree

   tree_out->Fill();

}


void DGAnalysis::analyzeGenParticles(const edm::Event& iEvent)
{

   std::cout << "Estoy dentro de analyze" << std::endl;

}


void DGAnalysis::analyzeDisplacedGlobal(const edm::Event& iEvent)
{

   nDG = 0;

   for (size_t i = 0; i < DisplacedGlobalCollection_->size(); i++)
   {

      const reco::Track &muon = (*DisplacedGlobalCollection_)[i];
      DG_pt[nDG] = muon.pt();
      DG_ptError[nDG] = muon.ptError();
      DG_eta[nDG] = muon.eta();
      DG_phi[nDG] = muon.phi();
      DG_q[nDG] = muon.charge();
      DG_numberOfValidHits[nDG] = muon.numberOfValidHits();
      DG_numberOfLostHits[nDG] = muon.numberOfLostHits();
      DG_chi2[nDG] = muon.chi2();
      DG_ndof[nDG] = muon.ndof();
      DG_normChi2[nDG] = muon.normalizedChi2();
    
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
      GM_q[nGM] = muon.charge();
      GM_numberOfValidHits[nGM] = muon.numberOfValidHits();
      GM_numberOfLostHits[nGM] = muon.numberOfLostHits();
      GM_chi2[nGM] = muon.chi2();
      GM_ndof[nGM] = muon.ndof();
      GM_normChi2[nGM] = muon.normalizedChi2();
    
      nGM++;

   }

}


