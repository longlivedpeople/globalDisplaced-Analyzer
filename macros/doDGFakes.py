import ROOT as r
from   ROOT import gROOT, TCanvas, TFile, TGraphErrors, SetOwnership, TVector3
import math, sys, optparse, array, copy, os
import gc, inspect
import numpy as np

import include.Canvas as Canvas

####################################### CLASS DEFINITION #########################################



runningfile = os.path.abspath(__file__)
WORKPATH = ''
for level in runningfile.split('/')[:-1]:
    WORKPATH += level
    WORKPATH += '/'

print('runningfile: ' + runningfile)

##################################### FUNCTION DEFINITION ########################################


if __name__ == "__main__":


    gROOT.ProcessLine('.L ' + WORKPATH + 'include/tdrstyle.C')
    gROOT.SetBatch(1)
    print('WORKPATH: ' + WORKPATH)
    r.setTDRStyle()

    ###########################
    ####   Parser object   ####
    ###########################
    parser = optparse.OptionParser(usage='usage: %prog [opts] FilenameWithSamples', version='%prog 1.0')
    parser.add_option('-t', '--tag', action='store', type=str, dest='tag', default='', help='Output tag')
    parser.add_option('-f', '--filename', action='store', type=str, dest='filename', default='', help='Path to file')
    parser.add_option('-m', '--nmax', action='store', type=int, dest='nmax', default=0, help='Path to file')
    parser.add_option('--etamax', action='store', type=float, dest='etamax', default=0.0, help='etamax')
    parser.add_option('--ptmin', action='store', type=float, dest='ptmin', default=0.0, help='ptmin')
    parser.add_option('--nhitmin', action='store', type=int, dest='nhitmin', default=0, help='ptmin')
    parser.add_option('--sigmaptmax', action='store', type=float, dest='sigmaptmax', default=0, help='sigmaptmax')
    parser.add_option('--normChi2max', action='store', type=float, dest='normChi2max', default=0.0, help='ptmin')
    (opts, args) = parser.parse_args()

    outputPath =  WORKPATH + 'fakes_muons/' if not opts.tag else WORKPATH + 'fakes_' + opts.tag + '/'

    ##################################
    ####   Variable declaration   ####
    ##################################
    MAX_DELTAR = 0.2 



    #################################
    ####   TEfficiency binning   ####
    #################################
    #Lxy_bin = np.array([0.0, 0.025, 0.5, 1.0, 2.0, 4.0, 8.0, 12.0, 16.0, 20., 30., 40., 50., 60., 70., 90., 110.0])
    #Lxy_bin = np.linspace(0.0, 110.0, 51)
    pt_bin = np.linspace(0.0, 300.0, 61)
    #ptSig_bin = np.linspace(0.0, 2.0, 50)
    ptSig_bin = np.array([0.0, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0, 1.4, 2.0])
    #pt_bin = np.concatenate((np.linspace(0, 125, 15), np.array([150, 175, 200, 250, 300, 400, 500])))
    eta_bin = np.linspace(-2.5, 2.5, 21)
    nvalid_bin = np.linspace(0, 90, 31)
    normChi2_bin = np.linspace(0, 15, 31)
    #dxy_bin = np.linspace(0, 30, 31)
    dxySep_bin = np.array([0.0, 1.0, 20.0, 100.0])
    dxy_bin = np.linspace(0, 100, 80)
    muonhit_bin = np.linspace(0, 10, 11)
    trackerhit_bin = np.linspace(0, 70, 71)

    #############################
    ####   Book Histograms   ####
    #############################

    ####
    #### DG HISTOGRAMS
    ####

    #### Total histograms:
    total_DG_pt = r.TH1F("total_DG_pt", ";Reconstructed #mu p_{T} (GeV);Muons", len(pt_bin)-1, pt_bin)
    total_DG_ptSig = r.TH1F("total_DG_ptSig", ";Reconstructed #mu #sigma_{pT}/p_{T} (GeV);Muons", len(ptSig_bin)-1, ptSig_bin)
    total_DG_eta = r.TH1F("total_DG_eta", ";Reconstructed #mu #eta;Muons", len(eta_bin)-1, eta_bin)
    total_DG_numberOfValidHits = r.TH1F("total_DG_numberOfValidHits", ";Number of valid hits;Muons", len(nvalid_bin)-1, nvalid_bin)
    total_DG_normChi2 = r.TH1F("total_DG_normChi2", ";Muon #chi^{2};Muons", len(normChi2_bin)-1, normChi2_bin)
    total_DG_dxy = r.TH1F("total_DG_dxy", ";Reconstructed d_{xy} (cm);Muons", len(dxy_bin)-1, dxy_bin)
    total_DG_nTR = r.TH1F("total_DG_nTR", ";Number of tracker hits;DG yield", len(trackerhit_bin)-1, trackerhit_bin)
    total_DG_nDT = r.TH1F("total_DG_nDT", ";Number of DT hits;DG yield", len(muonhit_bin)-1, muonhit_bin)
    total_DG_nRPC = r.TH1F("total_DG_nRPC", ";Number of RPC hits;DG yield", len(muonhit_bin)-1, muonhit_bin)
    total_DG_nCSC = r.TH1F("total_DG_nCSC", ";Number of CSC hits;DG yield", len(muonhit_bin)-1, muonhit_bin)

    #### Total histograms (bin1):
    total_DG_pt_bin1 = r.TH1F("total_DG_pt_bin1", ";Reconstructed #mu p_{T} (GeV);Muons", len(pt_bin)-1, pt_bin)
    total_DG_ptSig_bin1 = r.TH1F("total_DG_ptSig_bin1", ";Reconstructed #mu #sigma_{pT}/p_{T} (GeV);Muons", len(ptSig_bin)-1, ptSig_bin)
    total_DG_eta_bin1 = r.TH1F("total_DG_eta_bin1", ";Reconstructed #mu #eta;Muons", len(eta_bin)-1, eta_bin)
    total_DG_numberOfValidHits_bin1 = r.TH1F("total_DG_numberOfValidHits_bin1", ";Number of valid hits;Muons", len(nvalid_bin)-1, nvalid_bin)
    total_DG_normChi2_bin1 = r.TH1F("total_DG_normChi2_bin1", ";Muon #chi^{2};Muons", len(normChi2_bin)-1, normChi2_bin)

    #### Total histograms (bin2):
    total_DG_pt_bin2 = r.TH1F("total_DG_pt_bin2", ";Reconstructed #mu p_{T} (GeV);Muons", len(pt_bin)-1, pt_bin)
    total_DG_ptSig_bin2 = r.TH1F("total_DG_ptSig_bin2", ";Reconstructed #mu #sigma_{pT}/p_{T} (GeV);Muons", len(ptSig_bin)-1, ptSig_bin)
    total_DG_eta_bin2 = r.TH1F("total_DG_eta_bin2", ";Reconstructed #mu #eta;Muons", len(eta_bin)-1, eta_bin)
    total_DG_numberOfValidHits_bin2 = r.TH1F("total_DG_numberOfValidHits_bin2", ";Number of valid hits;Muons", len(nvalid_bin)-1, nvalid_bin)
    total_DG_normChi2_bin2 = r.TH1F("total_DG_normChi2_bin2", ";Muon #chi^{2};Muons", len(normChi2_bin)-1, normChi2_bin)

    #### Total histograms (bin3):
    total_DG_pt_bin3 = r.TH1F("total_DG_pt_bin3", ";Reconstructed #mu p_{T} (GeV);Muons", len(pt_bin)-1, pt_bin)
    total_DG_ptSig_bin3 = r.TH1F("total_DG_ptSig_bin3", ";Reconstructed #mu #sigma_{pT}/p_{T} (GeV);Muons", len(ptSig_bin)-1, ptSig_bin)
    total_DG_eta_bin3 = r.TH1F("total_DG_eta_bin3", ";Reconstructed #mu #eta;Muons", len(eta_bin)-1, eta_bin)
    total_DG_numberOfValidHits_bin3 = r.TH1F("total_DG_numberOfValidHits_bin3", ";Number of valid hits;Muons", len(nvalid_bin)-1, nvalid_bin)
    total_DG_normChi2_bin3 = r.TH1F("total_DG_normChi2_bin3", ";Muon #chi^{2};Muons", len(normChi2_bin)-1, normChi2_bin)



    #### Matched histograms:
    matched_DG_pt = r.TH1F("matched_DG_pt", ";Reconstructed #mu p_{T} (GeV);Muons", len(pt_bin)-1, pt_bin)
    matched_DG_ptSig = r.TH1F("matched_DG_ptSig", ";Reconstructed #mu #sigma_{pT}/p_{T} (GeV);Muons", len(ptSig_bin)-1, ptSig_bin)
    matched_DG_eta = r.TH1F("matched_DG_eta", ";Reconstructed #mu #eta;Muons", len(eta_bin)-1, eta_bin)
    matched_DG_numberOfValidHits = r.TH1F("matched_DG_numberOfValidHits", ";Number of valid hits;Muons", len(nvalid_bin)-1, nvalid_bin)
    matched_DG_normChi2 = r.TH1F("matched_DG_normChi2", ";Muon #chi^{2};Muons", len(normChi2_bin)-1, normChi2_bin)
    matched_DG_dxy = r.TH1F("matched_DG_dxy", ";Reconstructed d_{xy} (cm);Muons", len(dxy_bin)-1, dxy_bin)
    matched_DG_nTR = r.TH1F("matched_DG_nTR", ";Number of tracker hits;DG yield", len(trackerhit_bin)-1, trackerhit_bin)
    matched_DG_nDT = r.TH1F("matched_DG_nDT", ";Number of DT hits;DG yield", len(muonhit_bin)-1, muonhit_bin)
    matched_DG_nRPC = r.TH1F("matched_DG_nRPC", ";Number of RPC hits;DG yield", len(muonhit_bin)-1, muonhit_bin)
    matched_DG_nCSC = r.TH1F("matched_DG_nCSC", ";Number of CSC hits;DG yield", len(muonhit_bin)-1, muonhit_bin)


    #### Matched histograms (bin1):
    matched_DG_pt_bin1 = r.TH1F("matched_DG_pt_bin1", ";Reconstructed #mu p_{T} (GeV);Muons", len(pt_bin)-1, pt_bin)
    matched_DG_ptSig_bin1 = r.TH1F("matched_DG_ptSig_bin1", ";Reconstructed #mu #sigma_{pT}/p_{T} (GeV);Muons", len(ptSig_bin)-1, ptSig_bin)
    matched_DG_eta_bin1 = r.TH1F("matched_DG_eta_bin1", ";Reconstructed #mu #eta;Muons", len(eta_bin)-1, eta_bin)
    matched_DG_numberOfValidHits_bin1 = r.TH1F("matched_DG_numberOfValidHits_bin1", ";Number of valid hits;Muons", len(nvalid_bin)-1, nvalid_bin)
    matched_DG_normChi2_bin1 = r.TH1F("matched_DG_normChi2_bin1", ";Muon #chi^{2};Muons", len(normChi2_bin)-1, normChi2_bin)

    #### Matched histograms (bin2):
    matched_DG_pt_bin2 = r.TH1F("matched_DG_pt_bin2", ";Reconstructed #mu p_{T} (GeV);Muons", len(pt_bin)-1, pt_bin)
    matched_DG_ptSig_bin2 = r.TH1F("matched_DG_ptSig_bin2", ";Reconstructed #mu #sigma_{pT}/p_{T} (GeV);Muons", len(ptSig_bin)-1, ptSig_bin)
    matched_DG_eta_bin2 = r.TH1F("matched_DG_eta_bin2", ";Reconstructed #mu #eta;Muons", len(eta_bin)-1, eta_bin)
    matched_DG_numberOfValidHits_bin2 = r.TH1F("matched_DG_numberOfValidHits_bin2", ";Number of valid hits;Muons", len(nvalid_bin)-1, nvalid_bin)
    matched_DG_normChi2_bin2 = r.TH1F("matched_DG_normChi2_bin2", ";Muon #chi^{2};Muons", len(normChi2_bin)-1, normChi2_bin)

    #### Matched histograms (bin3):
    matched_DG_pt_bin3 = r.TH1F("matched_DG_pt_bin3", ";Reconstructed #mu p_{T} (GeV);Muons", len(pt_bin)-1, pt_bin)
    matched_DG_ptSig_bin3 = r.TH1F("matched_DG_ptSig_bin3", ";Reconstructed #mu #sigma_{pT}/p_{T} (GeV);Muons", len(ptSig_bin)-1, ptSig_bin)
    matched_DG_eta_bin3 = r.TH1F("matched_DG_eta_bin3", ";Reconstructed #mu #eta;Muons", len(eta_bin)-1, eta_bin)
    matched_DG_numberOfValidHits_bin3 = r.TH1F("matched_DG_numberOfValidHits_bin3", ";Number of valid hits;Muons", len(nvalid_bin)-1, nvalid_bin)
    matched_DG_normChi2_bin3 = r.TH1F("matched_DG_normChi2_bin3", ";Muon #chi^{2};Muons", len(normChi2_bin)-1, normChi2_bin)


    #### Unmatched histograms
    unmatched_DG_pt = r.TH1F("unmatched_DG_pt", ";Reconstructed #mu p_{T} (GeV);Muons", len(pt_bin)-1, pt_bin)
    unmatched_DG_ptSig = r.TH1F("unmatched_DG_ptSig", ";Reconstructed #mu #sigma_{pT}/p_{T} (GeV);Muons", len(ptSig_bin)-1, ptSig_bin)
    unmatched_DG_eta = r.TH1F("unmatched_DG_eta", ";Reconstructed #mu #eta;Muons", len(eta_bin)-1, eta_bin)
    unmatched_DG_numberOfValidHits = r.TH1F("unmatched_DG_numberOfValidHits", ";Number of valid hits;Muons", len(nvalid_bin)-1, nvalid_bin)
    unmatched_DG_normChi2 = r.TH1F("unmatched_DG_normChi2", ";Muon #chi^{2};Muons", len(normChi2_bin)-1, normChi2_bin)
    unmatched_DG_dxy = r.TH1F("unmatched_DG_dxy", ";Reconstructed d_{xy} (cm);Muons", len(dxy_bin)-1, dxy_bin)
    unmatched_DG_nTR = r.TH1F("unmatched_DG_nTR", ";Number of tracker hits;DG yield", len(trackerhit_bin)-1, trackerhit_bin)
    unmatched_DG_nDT = r.TH1F("unmatched_DG_nDT", ";Number of DT hits;DG yield", len(muonhit_bin)-1, muonhit_bin)
    unmatched_DG_nRPC = r.TH1F("unmatched_DG_nRPC", ";Number of RPC hits;DG yield", len(muonhit_bin)-1, muonhit_bin)
    unmatched_DG_nCSC = r.TH1F("unmatched_DG_nCSC", ";Number of CSC hits;DG yield", len(muonhit_bin)-1, muonhit_bin)

    #### Unmatched histograms (bin1):
    unmatched_DG_pt_bin1 = r.TH1F("unmatched_DG_pt_bin1", ";Reconstructed #mu p_{T} (GeV);Muons", len(pt_bin)-1, pt_bin)
    unmatched_DG_ptSig_bin1 = r.TH1F("unmatched_DG_ptSig_bin1", ";Reconstructed #mu #sigma_{pT}/p_{T} (GeV);Muons", len(ptSig_bin)-1, ptSig_bin)
    unmatched_DG_eta_bin1 = r.TH1F("unmatched_DG_eta_bin1", ";Reconstructed #mu #eta;Muons", len(eta_bin)-1, eta_bin)
    unmatched_DG_numberOfValidHits_bin1 = r.TH1F("unmatched_DG_numberOfValidHits_bin1", ";Number of valid hits;Muons", len(nvalid_bin)-1, nvalid_bin)
    unmatched_DG_normChi2_bin1 = r.TH1F("unmatched_DG_normChi2_bin1", ";Muon #chi^{2};Muons", len(normChi2_bin)-1, normChi2_bin)

    #### Unmatched histograms (bin2):
    unmatched_DG_pt_bin2 = r.TH1F("unmatched_DG_pt_bin2", ";Reconstructed #mu p_{T} (GeV);Muons", len(pt_bin)-1, pt_bin)
    unmatched_DG_ptSig_bin2 = r.TH1F("unmatched_DG_ptSig_bin2", ";Reconstructed #mu #sigma_{pT}/p_{T} (GeV);Muons", len(ptSig_bin)-1, ptSig_bin)
    unmatched_DG_eta_bin2 = r.TH1F("unmatched_DG_eta_bin2", ";Reconstructed #mu #eta;Muons", len(eta_bin)-1, eta_bin)
    unmatched_DG_numberOfValidHits_bin2 = r.TH1F("unmatched_DG_numberOfValidHits_bin2", ";Number of valid hits;Muons", len(nvalid_bin)-1, nvalid_bin)
    unmatched_DG_normChi2_bin2 = r.TH1F("unmatched_DG_normChi2_bin2", ";Muon #chi^{2};Muons", len(normChi2_bin)-1, normChi2_bin)

    #### Unmatched histograms (bin3):
    unmatched_DG_pt_bin3 = r.TH1F("unmatched_DG_pt_bin3", ";Reconstructed #mu p_{T} (GeV);Muons", len(pt_bin)-1, pt_bin)
    unmatched_DG_ptSig_bin3 = r.TH1F("unmatched_DG_ptSig_bin3", ";Reconstructed #mu #sigma_{pT}/p_{T} (GeV);Muons", len(ptSig_bin)-1, ptSig_bin)
    unmatched_DG_eta_bin3 = r.TH1F("unmatched_DG_eta_bin3", ";Reconstructed #mu #eta;Muons", len(eta_bin)-1, eta_bin)
    unmatched_DG_numberOfValidHits_bin3 = r.TH1F("unmatched_DG_numberOfValidHits_bin3", ";Number of valid hits;Muons", len(nvalid_bin)-1, nvalid_bin)
    unmatched_DG_normChi2_bin3 = r.TH1F("unmatched_DG_normChi2_bin3", ";Muon #chi^{2};Muons", len(normChi2_bin)-1, normChi2_bin)

    #### Predefined qeff rates
    normChi2_logbin = np.logspace(-1, 2, 60)
    pfake_DG_normChi2 = r.TEfficiency("pfake_DG_normChi2", ";;Fake rate", len(normChi2_logbin) -1, normChi2_logbin)

    #### 2D histograms
    matched_DG_sigmaptVSdxy = r.TH2F('matched_DG_sigmaptVSdxy', '; Transverse impact parameter |d_{xy}| (cm); DG resolution #sigma_{p_{T}}/p_{T};', 60, 0, 30, 30, 0, 2)
    

    #########################
    ####   Load sample   ####
    #########################

    _sampleNames = (opts.filename).split(',')
    _tree = r.TChain('Events')
    for _name in _sampleNames:
        _tree.Add(_name)

    print("TTree with " + str(_tree.GetEntries()) + " entries")

    ###################################
    ####   Loop over tree events   ####
    ###################################

    for i in range(0, _tree.GetEntries()):

        _tree.GetEntry(i)
        if opts.nmax and i > opts.nmax: break

        ### Muon Channel
        #if _tree.Flag_HLT_L2DoubleMu28_NoVertex_2Cha_Angle2p5_Mass10 == 1:
        if True:

            ###############
            ## DG muons ##
            ###############
            for j in range(0, _tree.nDG):
                #if abs(_tree.DG_eta[j]) > 2: continue
                #if _tree.DG_pt[j] < 31: continue

                pt       = _tree.DG_pt[j]
                ptSig    = _tree.DG_ptError[j]/_tree.DG_pt[j]
                eta      = _tree.DG_eta[j]
                phi      = _tree.DG_phi[j]
                dxy      = abs(_tree.DG_dxy[j])
                nvalid   = _tree.DG_numberOfValidHits[j]
                chi2     = _tree.DG_chi2[j]
                #ndof     = _tree.DG_ndof[j]
                normChi2 = _tree.DG_normChi2[j]
                """
                nTR = _tree.DG_nPB[j] + _tree.DG_nPE[j] + _tree.DG_nTIB[j] + _tree.DG_nTOB[j] + _tree.DG_nTID[j] + _tree.DG_nTEC[j]
                nRPC = _tree.DG_nRPC[j]
                nCSC = _tree.DG_nCSC[j]
                nDT = _tree.DG_nDT[j]
                """
                nTR = 0
                nRPC = 0
                nCSC = 0
                nDT = 0

                #if abs(eta) > 2: continue # default
                if opts.etamax and  abs(eta) > opts.etamax: continue # default
                if opts.ptmin and pt < opts.ptmin: continue
                if opts.nhitmin and nvalid < opts.nhitmin: continue
                if opts.normChi2max and normChi2 > opts.normChi2max: continue
                if opts.sigmaptmax and ptSig > opts.sigmaptmax: continue

                l = TVector3()
                l.SetPtEtaPhi(pt, eta, phi)

                total_DG_pt.Fill(pt)
                total_DG_ptSig.Fill(ptSig)
                total_DG_eta.Fill(eta)
                total_DG_dxy.Fill(dxy)
                total_DG_numberOfValidHits.Fill(nvalid)
                total_DG_normChi2.Fill(normChi2)
                total_DG_nTR.Fill(nTR)
                total_DG_nRPC.Fill(nRPC)
                total_DG_nDT.Fill(nDT)
                total_DG_nCSC.Fill(nCSC)

                if dxy < dxySep_bin[1]:
                    total_DG_pt_bin1.Fill(pt)
                    total_DG_ptSig_bin1.Fill(ptSig)
                    total_DG_eta_bin1.Fill(eta)
                    total_DG_numberOfValidHits_bin1.Fill(nvalid)
                    total_DG_normChi2_bin1.Fill(normChi2)
                elif dxy > dxySep_bin[1] and dxy < dxySep_bin[2]:
                    total_DG_pt_bin2.Fill(pt)
                    total_DG_ptSig_bin2.Fill(ptSig)
                    total_DG_eta_bin2.Fill(eta)
                    total_DG_numberOfValidHits_bin2.Fill(nvalid)
                    total_DG_normChi2_bin2.Fill(normChi2)
                elif dxy > dxySep_bin[2]:
                    total_DG_pt_bin3.Fill(pt)
                    total_DG_ptSig_bin3.Fill(ptSig)
                    total_DG_eta_bin3.Fill(eta)
                    total_DG_numberOfValidHits_bin3.Fill(nvalid)
                    total_DG_normChi2_bin3.Fill(normChi2)



                deltaR = 9999.0
                index = -9
                for k in range(0, _tree.ngenMu):

                    re = TVector3()
                    re.SetPtEtaPhi(_tree.genMu_pt[k], _tree.genMu_eta[k], _tree.genMu_phi[k])
                    if re.DeltaR(l) < deltaR:
                        deltaR = re.DeltaR(l)
                        index = k

                if deltaR < MAX_DELTAR:
                    matched_DG_pt.Fill(pt)
                    matched_DG_ptSig.Fill(ptSig)
                    matched_DG_eta.Fill(eta)
                    matched_DG_dxy.Fill(dxy)
                    matched_DG_numberOfValidHits.Fill(nvalid)
                    matched_DG_normChi2.Fill(normChi2)
                    pfake_DG_normChi2.Fill(False, normChi2)
                    matched_DG_sigmaptVSdxy.Fill(abs(dxy), ptSig)
                    matched_DG_nTR.Fill(nTR)
                    matched_DG_nRPC.Fill(nRPC)
                    matched_DG_nDT.Fill(nDT)
                    matched_DG_nCSC.Fill(nCSC)

                    if dxy < dxySep_bin[1]:
                        matched_DG_pt_bin1.Fill(pt)
                        matched_DG_ptSig_bin1.Fill(ptSig)
                        matched_DG_eta_bin1.Fill(eta)
                        matched_DG_numberOfValidHits_bin1.Fill(nvalid)
                        matched_DG_normChi2_bin1.Fill(normChi2)
                    elif dxy > dxySep_bin[1] and dxy < dxySep_bin[2]:
                        matched_DG_pt_bin2.Fill(pt)
                        matched_DG_ptSig_bin2.Fill(ptSig)
                        matched_DG_eta_bin2.Fill(eta)
                        matched_DG_numberOfValidHits_bin2.Fill(nvalid)
                        matched_DG_normChi2_bin2.Fill(normChi2)
                    elif dxy > dxySep_bin[2]:
                        matched_DG_pt_bin3.Fill(pt)
                        matched_DG_ptSig_bin3.Fill(ptSig)
                        matched_DG_eta_bin3.Fill(eta)
                        matched_DG_numberOfValidHits_bin3.Fill(nvalid)
                        matched_DG_normChi2_bin3.Fill(normChi2)
                else:
                    unmatched_DG_pt.Fill(pt)
                    unmatched_DG_ptSig.Fill(ptSig)
                    unmatched_DG_eta.Fill(eta)
                    unmatched_DG_dxy.Fill(dxy)
                    unmatched_DG_numberOfValidHits.Fill(nvalid)
                    unmatched_DG_normChi2.Fill(normChi2)
                    pfake_DG_normChi2.Fill(True, normChi2)
                    unmatched_DG_nTR.Fill(nTR)
                    unmatched_DG_nRPC.Fill(nRPC)
                    unmatched_DG_nDT.Fill(nDT)
                    unmatched_DG_nCSC.Fill(nCSC)

                    if dxy < dxySep_bin[1]:
                        unmatched_DG_pt_bin1.Fill(pt)
                        unmatched_DG_ptSig_bin1.Fill(ptSig)
                        unmatched_DG_eta_bin1.Fill(eta)
                        unmatched_DG_numberOfValidHits_bin1.Fill(nvalid)
                        unmatched_DG_normChi2_bin1.Fill(normChi2)
                    elif dxy > dxySep_bin[1] and dxy < dxySep_bin[2]:
                        unmatched_DG_pt_bin2.Fill(pt)
                        unmatched_DG_ptSig_bin2.Fill(ptSig)
                        unmatched_DG_eta_bin2.Fill(eta)
                        unmatched_DG_numberOfValidHits_bin2.Fill(nvalid)
                        unmatched_DG_normChi2_bin2.Fill(normChi2)
                    elif dxy > dxySep_bin[2]:
                        unmatched_DG_pt_bin3.Fill(pt)
                        unmatched_DG_ptSig_bin3.Fill(ptSig)
                        unmatched_DG_eta_bin3.Fill(eta)
                        unmatched_DG_numberOfValidHits_bin3.Fill(nvalid)
                        unmatched_DG_normChi2_bin3.Fill(normChi2)



    #### Define Fake rates
    fake_DG_pt = r.TEfficiency(unmatched_DG_pt, total_DG_pt)
    fake_DG_ptSig = r.TEfficiency(unmatched_DG_ptSig, total_DG_ptSig)
    fake_DG_eta = r.TEfficiency(unmatched_DG_eta, total_DG_eta)
    fake_DG_numberOfValidHits = r.TEfficiency(unmatched_DG_numberOfValidHits, total_DG_numberOfValidHits)
    fake_DG_normChi2 = r.TEfficiency(unmatched_DG_normChi2, total_DG_normChi2)
    fake_DG_nTR = r.TEfficiency(unmatched_DG_nTR, total_DG_nTR)
    fake_DG_nCSC = r.TEfficiency(unmatched_DG_nCSC, total_DG_nCSC)
    fake_DG_nRPC = r.TEfficiency(unmatched_DG_nRPC, total_DG_nRPC)
    fake_DG_nDT = r.TEfficiency(unmatched_DG_nDT, total_DG_nDT)

    fake_DG_pt_bin1 = r.TEfficiency(unmatched_DG_pt_bin1, total_DG_pt_bin1)
    fake_DG_ptSig_bin1 = r.TEfficiency(unmatched_DG_ptSig_bin1, total_DG_ptSig_bin1)
    fake_DG_eta_bin1 = r.TEfficiency(unmatched_DG_eta_bin1, total_DG_eta_bin1)
    fake_DG_numberOfValidHits_bin1 = r.TEfficiency(unmatched_DG_numberOfValidHits_bin1, total_DG_numberOfValidHits_bin1)
    fake_DG_normChi2_bin1 = r.TEfficiency(unmatched_DG_normChi2_bin1, total_DG_normChi2_bin1)

    fake_DG_pt_bin2 = r.TEfficiency(unmatched_DG_pt_bin2, total_DG_pt_bin2)
    fake_DG_ptSig_bin2 = r.TEfficiency(unmatched_DG_ptSig_bin2, total_DG_ptSig_bin2)
    fake_DG_eta_bin2 = r.TEfficiency(unmatched_DG_eta_bin2, total_DG_eta_bin2)
    fake_DG_numberOfValidHits_bin2 = r.TEfficiency(unmatched_DG_numberOfValidHits_bin2, total_DG_numberOfValidHits_bin2)
    fake_DG_normChi2_bin2 = r.TEfficiency(unmatched_DG_normChi2_bin2, total_DG_normChi2_bin2)

    fake_DG_pt_bin3 = r.TEfficiency(unmatched_DG_pt_bin3, total_DG_pt_bin3)
    fake_DG_ptSig_bin3 = r.TEfficiency(unmatched_DG_ptSig_bin3, total_DG_ptSig_bin3)
    fake_DG_eta_bin3 = r.TEfficiency(unmatched_DG_eta_bin3, total_DG_eta_bin3)
    fake_DG_numberOfValidHits_bin3 = r.TEfficiency(unmatched_DG_numberOfValidHits_bin3, total_DG_numberOfValidHits_bin3)
    fake_DG_normChi2_bin3 = r.TEfficiency(unmatched_DG_normChi2_bin3, total_DG_normChi2_bin3)

    fake_DG_dxy = r.TEfficiency(unmatched_DG_dxy, total_DG_dxy)


    #### Write everything to a file:

    if not os.path.exists(WORKPATH + 'fakes_'+opts.tag+'/'): os.makedirs(WORKPATH + 'fakes_'+opts.tag+'/')
    outputFile = TFile(WORKPATH +'fakes_'+ opts.tag + '/th1fs.root', 'RECREATE')

    total_DG_pt.Write()
    total_DG_ptSig.Write()
    total_DG_eta.Write()
    total_DG_dxy.Write()
    total_DG_numberOfValidHits.Write()
    total_DG_normChi2.Write()
    total_DG_nTR.Write()
    total_DG_nRPC.Write()
    total_DG_nDT.Write()
    total_DG_nCSC.Write()

    total_DG_pt_bin1.Write()
    total_DG_ptSig_bin1.Write()
    total_DG_eta_bin1.Write()
    total_DG_numberOfValidHits_bin1.Write()
    total_DG_normChi2_bin1.Write()

    total_DG_pt_bin2.Write()
    total_DG_ptSig_bin2.Write()
    total_DG_eta_bin2.Write()
    total_DG_numberOfValidHits_bin2.Write()
    total_DG_normChi2_bin2.Write()

    total_DG_pt_bin3.Write()
    total_DG_ptSig_bin3.Write()
    total_DG_eta_bin3.Write()
    total_DG_numberOfValidHits_bin3.Write()
    total_DG_normChi2_bin3.Write()

    matched_DG_pt.Write()
    matched_DG_ptSig.Write()
    matched_DG_eta.Write()
    matched_DG_dxy.Write()
    matched_DG_numberOfValidHits.Write()
    matched_DG_normChi2.Write()
    matched_DG_nTR.Write()
    matched_DG_nRPC.Write()
    matched_DG_nDT.Write()
    matched_DG_nCSC.Write()

    matched_DG_pt_bin1.Write()
    matched_DG_ptSig_bin1.Write()
    matched_DG_eta_bin1.Write()
    matched_DG_numberOfValidHits_bin1.Write()
    matched_DG_normChi2_bin1.Write()

    matched_DG_pt_bin2.Write()
    matched_DG_ptSig_bin2.Write()
    matched_DG_eta_bin2.Write()
    matched_DG_numberOfValidHits_bin2.Write()
    matched_DG_normChi2_bin2.Write()

    matched_DG_pt_bin3.Write()
    matched_DG_ptSig_bin3.Write()
    matched_DG_eta_bin3.Write()
    matched_DG_numberOfValidHits_bin3.Write()
    matched_DG_normChi2_bin3.Write()

    unmatched_DG_pt.Write()
    unmatched_DG_ptSig.Write()
    unmatched_DG_eta.Write()
    unmatched_DG_dxy.Write()
    unmatched_DG_numberOfValidHits.Write()
    unmatched_DG_normChi2.Write()
    unmatched_DG_nTR.Write()
    unmatched_DG_nRPC.Write()
    unmatched_DG_nDT.Write()
    unmatched_DG_nCSC.Write()

    unmatched_DG_pt_bin1.Write()
    unmatched_DG_ptSig_bin1.Write()
    unmatched_DG_eta_bin1.Write()
    unmatched_DG_numberOfValidHits_bin1.Write()
    unmatched_DG_normChi2_bin1.Write()

    unmatched_DG_pt_bin2.Write()
    unmatched_DG_ptSig_bin2.Write()
    unmatched_DG_eta_bin2.Write()
    unmatched_DG_numberOfValidHits_bin2.Write()
    unmatched_DG_normChi2_bin2.Write()

    unmatched_DG_pt_bin3.Write()
    unmatched_DG_ptSig_bin3.Write()
    unmatched_DG_eta_bin3.Write()
    unmatched_DG_numberOfValidHits_bin3.Write()
    unmatched_DG_normChi2_bin3.Write()

    fake_DG_pt.Write()
    fake_DG_ptSig.Write()
    fake_DG_eta.Write()
    fake_DG_numberOfValidHits.Write()
    fake_DG_normChi2.Write()
    pfake_DG_normChi2.Write()
    fake_DG_dxy.Write()
    fake_DG_nTR.Write()
    fake_DG_nRPC.Write()
    fake_DG_nCSC.Write()
    fake_DG_nDT.Write()

    fake_DG_pt_bin1.Write()
    fake_DG_ptSig_bin1.Write()
    fake_DG_eta_bin1.Write()
    fake_DG_numberOfValidHits_bin1.Write()
    fake_DG_normChi2_bin1.Write()
    fake_DG_pt_bin2.Write()
    fake_DG_ptSig_bin2.Write()
    fake_DG_eta_bin2.Write()
    fake_DG_numberOfValidHits_bin2.Write()
    fake_DG_normChi2_bin2.Write()
    fake_DG_pt_bin3.Write()
    fake_DG_ptSig_bin3.Write()
    fake_DG_eta_bin3.Write()
    fake_DG_numberOfValidHits_bin3.Write()
    fake_DG_normChi2_bin3.Write()

    matched_DG_sigmaptVSdxy.Write()

    outputFile.Close()
