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
    parser.add_option('--nMUmin', action='store', type=int, dest='nMUmin', default=0, help='nMUmin')
    parser.add_option('--nInTRmin', action='store', type=int, dest='nInTRmin', default=0, help='nInTRmin')
    parser.add_option('--nOutTRmin', action='store', type=int, dest='nOutTRmin', default=0, help='nOutTRmin')
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
    pt_bin = np.linspace(0.0, 300.0, 61)
    ptSig_bin = np.array([0.0, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0, 1.4, 2.0])
    ptSig_bin = np.logspace(-3, 2, 50)
    eta_bin = np.linspace(-3.0, 3.0, 61)
    nvalid_bin = np.linspace(0, 90, 91)
    normChi2_bin = np.linspace(0, 15, 31)
    muonhit_bin = np.linspace(0, 50, 51)
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
    total_DG_nTR = r.TH1F("total_DG_nTR", ";Number of tracker hits;DG yield", len(trackerhit_bin)-1, trackerhit_bin)
    total_DG_nInTR = r.TH1F("total_DG_nInTR", ";Number of tracker hits;DG yield", len(trackerhit_bin)-1, trackerhit_bin)
    total_DG_nOutTR = r.TH1F("total_DG_nOutTR", ";Number of tracker hits;DG yield", len(trackerhit_bin)-1, trackerhit_bin)
    total_DG_nDT = r.TH1F("total_DG_nDT", ";Number of DT hits;DG yield", len(muonhit_bin)-1, muonhit_bin)
    total_DG_nRPC = r.TH1F("total_DG_nRPC", ";Number of RPC hits;DG yield", len(muonhit_bin)-1, muonhit_bin)
    total_DG_nCSC = r.TH1F("total_DG_nCSC", ";Number of CSC hits;DG yield", len(muonhit_bin)-1, muonhit_bin)
    total_DG_nMU = r.TH1F("total_DG_nMU", ";Number of MU hits;DG yield", len(muonhit_bin)-1, muonhit_bin)


    #### Matched histograms:
    matched_DG_pt = r.TH1F("matched_DG_pt", ";Reconstructed #mu p_{T} (GeV);Muons", len(pt_bin)-1, pt_bin)
    matched_DG_ptSig = r.TH1F("matched_DG_ptSig", ";Reconstructed #mu #sigma_{pT}/p_{T} (GeV);Muons", len(ptSig_bin)-1, ptSig_bin)
    matched_DG_eta = r.TH1F("matched_DG_eta", ";Reconstructed #mu #eta;Muons", len(eta_bin)-1, eta_bin)
    matched_DG_numberOfValidHits = r.TH1F("matched_DG_numberOfValidHits", ";Number of valid hits;Muons", len(nvalid_bin)-1, nvalid_bin)
    matched_DG_normChi2 = r.TH1F("matched_DG_normChi2", ";Muon #chi^{2};Muons", len(normChi2_bin)-1, normChi2_bin)
    matched_DG_nTR = r.TH1F("matched_DG_nTR", ";Number of tracker hits;DG yield", len(trackerhit_bin)-1, trackerhit_bin)
    matched_DG_nInTR = r.TH1F("matched_DG_nInTR", ";Number of tracker hits;DG yield", len(trackerhit_bin)-1, trackerhit_bin)
    matched_DG_nOutTR = r.TH1F("matched_DG_nOutTR", ";Number of tracker hits;DG yield", len(trackerhit_bin)-1, trackerhit_bin)
    matched_DG_nDT = r.TH1F("matched_DG_nDT", ";Number of DT hits;DG yield", len(muonhit_bin)-1, muonhit_bin)
    matched_DG_nRPC = r.TH1F("matched_DG_nRPC", ";Number of RPC hits;DG yield", len(muonhit_bin)-1, muonhit_bin)
    matched_DG_nCSC = r.TH1F("matched_DG_nCSC", ";Number of CSC hits;DG yield", len(muonhit_bin)-1, muonhit_bin)
    matched_DG_nMU = r.TH1F("matched_DG_nMU", ";Number of MU hits;DG yield", len(muonhit_bin)-1, muonhit_bin)


    #### Unmatched histograms
    unmatched_DG_pt = r.TH1F("unmatched_DG_pt", ";Reconstructed #mu p_{T} (GeV);Muons", len(pt_bin)-1, pt_bin)
    unmatched_DG_ptSig = r.TH1F("unmatched_DG_ptSig", ";Reconstructed #mu #sigma_{pT}/p_{T} (GeV);Muons", len(ptSig_bin)-1, ptSig_bin)
    unmatched_DG_eta = r.TH1F("unmatched_DG_eta", ";Reconstructed #mu #eta;Muons", len(eta_bin)-1, eta_bin)
    unmatched_DG_numberOfValidHits = r.TH1F("unmatched_DG_numberOfValidHits", ";Number of valid hits;Muons", len(nvalid_bin)-1, nvalid_bin)
    unmatched_DG_normChi2 = r.TH1F("unmatched_DG_normChi2", ";Muon #chi^{2};Muons", len(normChi2_bin)-1, normChi2_bin)
    unmatched_DG_nTR = r.TH1F("unmatched_DG_nTR", ";Number of tracker hits;DG yield", len(trackerhit_bin)-1, trackerhit_bin)
    unmatched_DG_nInTR = r.TH1F("unmatched_DG_nInTR", ";Number of tracker hits;DG yield", len(trackerhit_bin)-1, trackerhit_bin)
    unmatched_DG_nOutTR = r.TH1F("unmatched_DG_nOutTR", ";Number of tracker hits;DG yield", len(trackerhit_bin)-1, trackerhit_bin)
    unmatched_DG_nDT = r.TH1F("unmatched_DG_nDT", ";Number of DT hits;DG yield", len(muonhit_bin)-1, muonhit_bin)
    unmatched_DG_nRPC = r.TH1F("unmatched_DG_nRPC", ";Number of RPC hits;DG yield", len(muonhit_bin)-1, muonhit_bin)
    unmatched_DG_nCSC = r.TH1F("unmatched_DG_nCSC", ";Number of CSC hits;DG yield", len(muonhit_bin)-1, muonhit_bin)
    unmatched_DG_nMU = r.TH1F("unmatched_DG_nMU", ";Number of MU hits;DG yield", len(muonhit_bin)-1, muonhit_bin)



    #########################
    ####   Load sample   ####
    #########################

    _dirName = opts.filename
    _tree = r.TChain('Events')
    for _file in os.listdir(_dirName):
        if '.root' not in _file: continue
        _tree.Add(_dirName + _file)

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

                pt       = _tree.DG_pt[j]
                ptSig    = _tree.DG_ptError[j]/_tree.DG_pt[j]
                eta      = _tree.DG_eta[j]
                phi      = _tree.DG_phi[j]
                dxy      = abs(_tree.DG_dxy[j])
                nvalid   = _tree.DG_numberOfValidHits[j]
                chi2     = _tree.DG_chi2[j]
                #ndof     = _tree.DG_ndof[j]
                normChi2 = _tree.DG_normChi2[j]
                nTR = _tree.DG_nPB[j] + _tree.DG_nPE[j] + _tree.DG_nTIB[j] + _tree.DG_nTOB[j] + _tree.DG_nTID[j] + _tree.DG_nTEC[j]
                nInTR = _tree.DG_nPB[j] + _tree.DG_nPE[j] 
                nOutTR = _tree.DG_nTIB[j] + _tree.DG_nTOB[j] + _tree.DG_nTID[j] + _tree.DG_nTEC[j]
                nRPC = _tree.DG_nRPC[j]
                nCSC = _tree.DG_nCSC[j]
                nDT = _tree.DG_nDT[j]
                nMU = nRPC + nDT + nCSC

                if opts.etamax and  abs(eta) > opts.etamax: continue # default
                if opts.ptmin and pt < opts.ptmin: continue
                if opts.nhitmin and nvalid < opts.nhitmin: continue
                if opts.nMUmin and nMU < opts.nMUmin: continue
                if opts.nInTRmin and nInTR < opts.nInTRmin: continue
                if opts.nOutTRmin and nOutTR < opts.nOutTRmin: continue
                if opts.normChi2max and normChi2 > opts.normChi2max: continue
                if opts.sigmaptmax and ptSig > opts.sigmaptmax: continue

                l = TVector3()
                l.SetPtEtaPhi(pt, eta, phi)

                total_DG_pt.Fill(pt)
                total_DG_ptSig.Fill(ptSig)
                total_DG_eta.Fill(eta)
                total_DG_numberOfValidHits.Fill(nvalid)
                total_DG_normChi2.Fill(normChi2)
                total_DG_nTR.Fill(nTR)
                total_DG_nInTR.Fill(nInTR)
                total_DG_nOutTR.Fill(nOutTR)
                total_DG_nRPC.Fill(nRPC)
                total_DG_nDT.Fill(nDT)
                total_DG_nCSC.Fill(nCSC)
                total_DG_nMU.Fill(nMU)


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
                    matched_DG_numberOfValidHits.Fill(nvalid)
                    matched_DG_normChi2.Fill(normChi2)
                    matched_DG_nTR.Fill(nTR)
                    matched_DG_nInTR.Fill(nInTR)
                    matched_DG_nOutTR.Fill(nOutTR)
                    matched_DG_nRPC.Fill(nRPC)
                    matched_DG_nDT.Fill(nDT)
                    matched_DG_nCSC.Fill(nCSC)
                    matched_DG_nMU.Fill(nMU)

                else:
                    unmatched_DG_pt.Fill(pt)
                    unmatched_DG_ptSig.Fill(ptSig)
                    unmatched_DG_eta.Fill(eta)
                    unmatched_DG_numberOfValidHits.Fill(nvalid)
                    unmatched_DG_normChi2.Fill(normChi2)
                    unmatched_DG_nTR.Fill(nTR)
                    unmatched_DG_nInTR.Fill(nInTR)
                    unmatched_DG_nOutTR.Fill(nOutTR)
                    unmatched_DG_nRPC.Fill(nRPC)
                    unmatched_DG_nDT.Fill(nDT)
                    unmatched_DG_nCSC.Fill(nCSC)
                    unmatched_DG_nMU.Fill(nMU)


    #### Define Fake rates
    fake_DG_pt = r.TEfficiency(unmatched_DG_pt, total_DG_pt)
    fake_DG_ptSig = r.TEfficiency(unmatched_DG_ptSig, total_DG_ptSig)
    fake_DG_eta = r.TEfficiency(unmatched_DG_eta, total_DG_eta)
    fake_DG_numberOfValidHits = r.TEfficiency(unmatched_DG_numberOfValidHits, total_DG_numberOfValidHits)
    fake_DG_normChi2 = r.TEfficiency(unmatched_DG_normChi2, total_DG_normChi2)
    fake_DG_nTR = r.TEfficiency(unmatched_DG_nTR, total_DG_nTR)
    fake_DG_nInTR = r.TEfficiency(unmatched_DG_nInTR, total_DG_nInTR)
    fake_DG_nOutTR = r.TEfficiency(unmatched_DG_nOutTR, total_DG_nOutTR)
    fake_DG_nCSC = r.TEfficiency(unmatched_DG_nCSC, total_DG_nCSC)
    fake_DG_nRPC = r.TEfficiency(unmatched_DG_nRPC, total_DG_nRPC)
    fake_DG_nDT = r.TEfficiency(unmatched_DG_nDT, total_DG_nDT)
    fake_DG_nMU = r.TEfficiency(unmatched_DG_nMU, total_DG_nMU)



    #### Write everything to a file:

    if not os.path.exists(WORKPATH + 'fakes_'+opts.tag+'/'): os.makedirs(WORKPATH + 'fakes_'+opts.tag+'/')
    outputFile = TFile(WORKPATH +'fakes_'+ opts.tag + '/th1fs.root', 'RECREATE')

    total_DG_pt.Write()
    total_DG_ptSig.Write()
    total_DG_eta.Write()
    total_DG_numberOfValidHits.Write()
    total_DG_normChi2.Write()
    total_DG_nTR.Write()
    total_DG_nInTR.Write()
    total_DG_nOutTR.Write()
    total_DG_nRPC.Write()
    total_DG_nDT.Write()
    total_DG_nCSC.Write()
    total_DG_nMU.Write()


    matched_DG_pt.Write()
    matched_DG_ptSig.Write()
    matched_DG_eta.Write()
    matched_DG_numberOfValidHits.Write()
    matched_DG_normChi2.Write()
    matched_DG_nTR.Write()
    matched_DG_nInTR.Write()
    matched_DG_nOutTR.Write()
    matched_DG_nRPC.Write()
    matched_DG_nDT.Write()
    matched_DG_nCSC.Write()
    matched_DG_nMU.Write()

    unmatched_DG_pt.Write()
    unmatched_DG_ptSig.Write()
    unmatched_DG_eta.Write()
    unmatched_DG_numberOfValidHits.Write()
    unmatched_DG_normChi2.Write()
    unmatched_DG_nTR.Write()
    unmatched_DG_nInTR.Write()
    unmatched_DG_nOutTR.Write()
    unmatched_DG_nRPC.Write()
    unmatched_DG_nDT.Write()
    unmatched_DG_nCSC.Write()
    unmatched_DG_nMU.Write()


    fake_DG_pt.Write()
    fake_DG_ptSig.Write()
    fake_DG_eta.Write()
    fake_DG_numberOfValidHits.Write()
    fake_DG_normChi2.Write()
    fake_DG_nTR.Write()
    fake_DG_nInTR.Write()
    fake_DG_nOutTR.Write()
    fake_DG_nRPC.Write()
    fake_DG_nCSC.Write()
    fake_DG_nDT.Write()
    fake_DG_nMU.Write()


    outputFile.Close()
