#ifndef DGAnalysis_H
#define DGAnalysis_H

#include <memory>

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

// Generation
#include "SimDataFormats/GeneratorProducts/interface/HepMCProduct.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "SimDataFormats/GeneratorProducts/interface/GenRunInfoProduct.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "DataFormats/RecoCandidate/interface/RecoCandidate.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

// Utils
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "TrackingTools/TransientTrack/interface/TransientTrack.h"

// DisplacedGlobal handling
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"

// STDLIB
#include <string>
#include <iostream>
#include <vector>
#include <algorithm>

// ROOT
#include "TLorentzVector.h"
#include "TTree.h"
#include "TFile.h"


class DGAnalysis : public edm::one::EDAnalyzer<edm::one::SharedResources>  {
   public:
      explicit DGAnalysis(const edm::ParameterSet&);
      ~DGAnalysis();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:
      virtual void beginJob() override;
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;

      virtual void analyzeGenParticles(edm::Event const& e);
      virtual void analyzeDisplacedGlobal(edm::Event const& e);
      virtual void analyzeGlobalMuons(edm::Event const& e);


      edm::ParameterSet parameters;
      std::string output_filename;

      //
      // --- Tokens and Handles
      //

      // MC truth
      edm::EDGetTokenT<edm::View<reco::GenParticle> >  GenParticleToken_;
      edm::Handle<edm::View<reco::GenParticle> > GenParticleCollection_;

      // Displaced Global Muons
      edm::EDGetTokenT<edm::View<reco::Track> > DisplacedGlobalToken_;
      edm::Handle<edm::View<reco::Track> > DisplacedGlobalCollection_;


      // Standard Global Muons
      edm::EDGetTokenT<edm::View<reco::Track> > GlobalMuonToken_;
      edm::Handle<edm::View<reco::Track> > GlobalMuonCollection_;


      //
      // --- Variables used
      //

      // Event info
      Int_t eventId;
      Int_t luminosityBlock;
      Int_t run;

      // Pileup
      Int_t nPU;
      Int_t nPUTrue;

      // Primary vertex
      Float_t PV_vx;
      Float_t PV_vy;
      Float_t PV_vz;

      // Generated muons
      Int_t ngenMu;
      Float_t genMu_pt[100];
      Float_t genMu_eta[100];
      Float_t genMu_phi[100];
      Float_t genMu_dxy[100];
      Float_t genMu_vx[100];
      Float_t genMu_vy[100];
      Float_t genMu_vz[100];
      Int_t genMu_pdgId[100];
      Int_t genMu_motherPdgId[100];
      Int_t genMu_isPromptFinalState[100];
      Int_t genMu_isDirectPromptTauDecayProductFinalState[100];
      Int_t genMu_isDirectHadronDecayProduct[100];

      // Displaced Global Muons
      Int_t nDG = 0;
      Float_t DG_pt[200] = {0};
      Float_t DG_ptError[200] = {0};
      Float_t DG_eta[200] = {0};
      Float_t DG_phi[200] = {0};
      Float_t DG_dxy[200] = {0};
      Float_t DG_dxyError[200] = {0};
      Float_t DG_Ixy[200] = {0};
      Int_t DG_q[200] = {0};
      Int_t DG_numberOfValidHits[200] = {0};
      Int_t DG_numberOfLostHits[200] = {0};
      Float_t DG_chi2[200] = {0};
      Float_t DG_ndof[200] = {0};
      Float_t DG_normChi2[200] = {0};

      // Global Muons
      Int_t nGM = 0;
      Float_t GM_pt[200] = {0};
      Float_t GM_ptError[200] = {0};
      Float_t GM_eta[200] = {0};
      Float_t GM_phi[200] = {0};
      Float_t GM_dxy[200] = {0};
      Float_t GM_dxyError[200] = {0};
      Float_t GM_Ixy[200] = {0};
      Float_t GM_q[200] = {0};
      Int_t GM_numberOfValidHits[200] = {0};
      Int_t GM_numberOfLostHits[200] = {0};
      Float_t GM_chi2[200] = {0};
      Float_t GM_ndof[200] = {0};
      Float_t GM_normChi2[200] = {0};
      


      // Output definition
      TFile *file_out;
      TTree *tree_out;

};

#endif





