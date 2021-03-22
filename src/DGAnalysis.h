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
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "RecoVertex/VertexPrimitives/interface/TransientVertex.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/PatCandidates/interface/TriggerObjectStandAlone.h"
#include "DataFormats/PatCandidates/interface/PackedTriggerPrescales.h"


// DisplacedGlobal handling
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"

// Jets
#include "DataFormats/JetReco/interface/GenJet.h"
#include "DataFormats/PatCandidates/interface/Jet.h"


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
      virtual void analyzeDisplacedStandalone(edm::Event const& e);
      virtual void analyzeJets(edm::Event const& e);
      virtual void analyzeGenJets(edm::Event const& e);
      virtual TrajectoryStateClosestToPoint computeTrajectory(const reco::Track &track);
      std::string getPathVersion(const edm:: TriggerNames &names, const std::string &rawPath);


      edm::ParameterSet parameters;
      std::string output_filename;

      //
      // --- Tokens and Handles
      //

      // HLT
      edm::EDGetTokenT<edm::TriggerResults>  TriggerBitsToken_;
      edm::Handle<edm::TriggerResults> triggerBits_;

      // PU summary
      edm::EDGetTokenT<std::vector<PileupSummaryInfo> >  PUSummaryToken_;
      edm::Handle<std::vector<PileupSummaryInfo> > puInfoH_;

      // PV
      edm::EDGetTokenT<edm::View<reco::Vertex> >  PVToken_;
      edm::Handle<edm::View<reco::Vertex> > PVCollection_;

      // MC truth
      edm::EDGetTokenT<edm::View<reco::GenParticle> >  GenParticleToken_;
      edm::Handle<edm::View<reco::GenParticle> > GenParticleCollection_;

      // Displaced Global Muons
      edm::EDGetTokenT<edm::View<reco::Track> > DisplacedGlobalToken_;
      edm::Handle<edm::View<reco::Track> > DisplacedGlobalCollection_;

      // Displaced Global Muons
      edm::EDGetTokenT<edm::View<reco::Track> > DisplacedStandaloneToken_;
      edm::Handle<edm::View<reco::Track> > DisplacedStandaloneCollection_;

      // Standard Global Muons
      edm::EDGetTokenT<edm::View<reco::Track> > GlobalMuonToken_;
      edm::Handle<edm::View<reco::Track> > GlobalMuonCollection_;

      // Jets
      edm::EDGetTokenT<edm::View<reco::GenJet> > GenJetToken_;
      edm::Handle<edm::View<reco::GenJet> > GenJetCollection_;

      edm::EDGetTokenT<edm::View<pat::Jet> > JetToken_;
      edm::Handle<edm::View<pat::Jet> > JetCollection_;

      // Transient track builder
      edm::ESHandle<TransientTrackBuilder> TransientTrackBuilder_;


      //
      // --- Variables used
      //

      // Event info
      Int_t eventId = 0;
      Int_t luminosityBlock = 0;
      Int_t run = 0;

      // HLT
      bool Flag_HLT_IsoMu24 = false;


      // Pileup
      Int_t nPU = 0;
      Int_t nPUTrue = 0;

      // Primary vertex
      Float_t PV_vx = 0.;
      Float_t PV_vy = 0.;
      Float_t PV_vz = 0.;

      // Generated muons
      Int_t ngenMu = 0;
      Float_t genMu_pt[100] = {0};
      Float_t genMu_eta[100] = {0};
      Float_t genMu_phi[100] = {0};
      Float_t genMu_dxy[100] = {0};
      Float_t genMu_dxy0[100] = {0};
      Float_t genMu_dz[100] = {0};
      Float_t genMu_dz0[100] = {0};
      Float_t genMu_vx[100] = {0};
      Float_t genMu_vy[100] = {0};
      Float_t genMu_vz[100] = {0};
      Int_t genMu_pdgId[100] = {0};
      Int_t genMu_motherPdgId[100] = {0};
      Int_t genMu_isPromptFinalState[100] = {0};
      Int_t genMu_isDirectPromptTauDecayProductFinalState[100] = {0};
      Int_t genMu_isDirectHadronDecayProduct[100] = {0};

      // Displaced Global Muons
      Int_t nDG = 0;
      Float_t DG_pt[200] = {0};
      Float_t DG_ptError[200] = {0};
      Float_t DG_eta[200] = {0};
      Float_t DG_phi[200] = {0};
      Float_t DG_vx[200] = {0};
      Float_t DG_vy[200] = {0};
      Float_t DG_vz[200] = {0};
      Float_t DG_dxy[200] = {0};
      Float_t DG_dxy0[200] = {0}; 
      Float_t DG_dxy0Error[200] = {0};
      Float_t DG_dxyError[200] = {0};
      Float_t DG_Ixy[200] = {0};
      Float_t DG_dz[200] = {0};
      Float_t DG_dz0[200] = {0};
      Float_t DG_dzError[200] = {0};
      Float_t DG_dz0Error[200] = {0};
      Float_t DG_Iz[200] = {0};
      Int_t DG_q[200] = {0};
      Int_t DG_numberOfValidHits[200] = {0};
      Int_t DG_numberOfLostHits[200] = {0};
      Float_t DG_chi2[200] = {0};
      Float_t DG_ndof[200] = {0};
      Float_t DG_normChi2[200] = {0};
      Int_t DG_nPB[200] = {0};
      Int_t DG_nPE[200] = {0};
      Int_t DG_nTIB[200] = {0};
      Int_t DG_nTOB[200] = {0};
      Int_t DG_nTID[200] = {0};
      Int_t DG_nTEC[200] = {0};
      Int_t DG_nDT[200] = {0};
      Int_t DG_nCSC[200] = {0};
      Int_t DG_nRPC[200] = {0};
      Int_t DG_nGEM[200] = {0};
      Int_t DG_nME0[200] = {0};
      Int_t DG_muonStations[200] = {0};
      Int_t DG_muonHits[200] = {0};
      Int_t DG_outerTrackerHits[200] = {0};
      Int_t DG_trackerHits[200] = {0};
      Int_t DG_totalHits[200] = {0};
      Int_t DG_DTHits[200] = {0};
      Int_t DG_CSCHits[200] = {0};

      // Global Muons
      Int_t nGM = 0;
      Float_t GM_pt[200] = {0};
      Float_t GM_ptError[200] = {0};
      Float_t GM_eta[200] = {0};
      Float_t GM_phi[200] = {0};
      Float_t GM_vx[200] = {0};
      Float_t GM_vy[200] = {0};
      Float_t GM_vz[200] = {0};
      Float_t GM_dxy[200] = {0};
      Float_t GM_dxy0[200] = {0};
      Float_t GM_dxy0Error[200] = {0};
      Float_t GM_dxyError[200] = {0};
      Float_t GM_Ixy[200] = {0};
      Float_t GM_dz[200] = {0};
      Float_t GM_dz0[200] = {0};
      Float_t GM_dzError[200] = {0};
      Float_t GM_dz0Error[200] = {0};
      Float_t GM_Iz[200] = {0};
      Float_t GM_q[200] = {0};
      Int_t GM_numberOfValidHits[200] = {0};
      Int_t GM_numberOfLostHits[200] = {0};
      Float_t GM_chi2[200] = {0};
      Float_t GM_ndof[200] = {0};
      Float_t GM_normChi2[200] = {0};
      
      // Displaced Standalone Muons
      Int_t nDSA = 0;
      Float_t DSA_pt[200] = {0};
      Float_t DSA_ptError[200] = {0};
      Float_t DSA_eta[200] = {0};
      Float_t DSA_phi[200] = {0};
      Float_t DSA_vx[200] = {0};
      Float_t DSA_vy[200] = {0};
      Float_t DSA_vz[200] = {0};
      Float_t DSA_dxy[200] = {0};
      Float_t DSA_dxy0[200] = {0}; 
      Float_t DSA_dxy0Error[200] = {0};
      Float_t DSA_dxyError[200] = {0};
      Float_t DSA_Ixy[200] = {0};
      Float_t DSA_dz[200] = {0};
      Float_t DSA_dz0[200] = {0};
      Float_t DSA_dzError[200] = {0};
      Float_t DSA_dz0Error[200] = {0};
      Float_t DSA_Iz[200] = {0};
      Int_t DSA_q[200] = {0};
      Int_t DSA_numberOfValidHits[200] = {0};
      Int_t DSA_numberOfLostHits[200] = {0};
      Float_t DSA_chi2[200] = {0};
      Float_t DSA_ndof[200] = {0};
      Float_t DSA_normChi2[200] = {0};

      // Jets
      Int_t nJet = 0;
      Float_t Jet_pt[200] = {0};
      Float_t Jet_eta[200] = {0};
      Float_t Jet_phi[200] = {0};

      // GenJets
      Int_t nGenJet = 0;
      Float_t GenJet_pt[200] = {0};
      Float_t GenJet_eta[200] = {0};
      Float_t GenJet_phi[200] = {0};

      // Output definition
      TFile *file_out;
      TTree *tree_out;

};

#endif






