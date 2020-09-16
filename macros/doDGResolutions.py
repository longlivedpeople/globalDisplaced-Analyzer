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
    parser.add_option('--ptmin', action='store', type=float, dest='ptmin', default=0.0, help='ptmin')
    parser.add_option('--nhitmin', action='store', type=int, dest='nhitmin', default=0, help='ptmin')
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
    ptres_bin = np.linspace(-1, 1, 100)
    sigmapt_sep = np.array([0.0, 0.5, 1.0])
    normChi2_sep = np.array([0.0, 5.0])
    sigmapt_bin = np.linspace(0, 5, 60)
    normChi2_bin = np.linspace(0, 15, 60)

    #############################
    ####   Book Histograms   ####
    #############################

    ####
    #### DG HISTOGRAMS
    ####

    #### respt histograms:
    ptres_DG = r.TH1F("ptres_DG", ";(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{gen};", len(ptres_bin)-1, ptres_bin)
    ptres_DG_sigmapt_bin1 = r.TH1F("ptres_DG_sigmapt_bin1", ";(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{gen};", len(ptres_bin)-1, ptres_bin)
    ptres_DG_sigmapt_bin2 = r.TH1F("ptres_DG_sigmapt_bin2", ";(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{gen};", len(ptres_bin)-1, ptres_bin)
    #ptres_DG_sigmapt_bin3 = r.TH1F("ptres_DG_sigmapt_bin3", ";(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{gen};", len(ptres_bin)-1, ptres_bin)

    ptres_DG_normChi2_bin1 = r.TH1F("ptres_DG_normChi2_bin1", ";(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{gen};", len(ptres_bin)-1, ptres_bin)
    ptres_DG_normChi2_bin2 = r.TH1F("ptres_DG_normChi2_bin2", ";(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{gen};", len(ptres_bin)-1, ptres_bin)

    hist_DG_sigmapt = r.TH1F("hist_DG_sigmapt", ";DG #sigma_{pT}/p_{T};Muon yield", len(sigmapt_bin)-1, sigmapt_bin)
    hist_DG_normChi2 = r.TH1F("hist_DG_normChi2", ";DG #chi^{2}/ndof;Muon yield", len(normChi2_bin)-1, normChi2_bin)

    

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

                if abs(eta) > 2: continue # default
                if opts.ptmin and pt < opts.ptmin: continue
                if opts.nhitmin and nvalid < opts.nhitmin: continue
                if opts.normChi2max and normChi2 > opts.normChi2max: continue

                l = TVector3()
                l.SetPtEtaPhi(pt, eta, phi)

                deltaR = 9999.0
                index = -9
                for k in range(0, _tree.ngenMu):

                    re = TVector3()
                    re.SetPtEtaPhi(_tree.genMu_pt[k], _tree.genMu_eta[k], _tree.genMu_phi[k])
                    if re.DeltaR(l) < deltaR:
                        deltaR = re.DeltaR(l)
                        index = k

                if deltaR < MAX_DELTAR:
                    
                    ptres = (_tree.genMu_pt[index] - pt)/pt
                    
                    hist_DG_sigmapt.Fill(ptSig)
                    hist_DG_normChi2.Fill(normChi2)

                    ## sigmapt binning:
                    if ptSig < sigmapt_sep[1]:
                        ptres_DG_sigmapt_bin1.Fill(ptres) 
                    elif ptSig > sigmapt_sep[1]:
                        ptres_DG_sigmapt_bin2.Fill(ptres) 

                    ## normChi2 binning:
                    if normChi2 < normChi2_sep[1]:
                        ptres_DG_normChi2_bin1.Fill(ptres) 
                    elif normChi2 > normChi2_sep[1]:
                        ptres_DG_normChi2_bin2.Fill(ptres) 

    #### Write everything to a file:

    if not os.path.exists(WORKPATH + 'resolutions_'+opts.tag+'/'): os.makedirs(WORKPATH + 'resolutions_'+opts.tag+'/')
    outputFile = TFile(WORKPATH +'resolutions_'+ opts.tag + '/th1fs.root', 'RECREATE')

    hist_DG_sigmapt.Write()
    hist_DG_normChi2.Write()

    ptres_DG_sigmapt_bin1.Write()
    ptres_DG_sigmapt_bin2.Write()

    ptres_DG_normChi2_bin1.Write()
    ptres_DG_normChi2_bin2.Write()

    outputFile.Close()
