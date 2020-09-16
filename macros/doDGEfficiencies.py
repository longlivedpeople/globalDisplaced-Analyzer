import ROOT as r
from   ROOT import gROOT, TCanvas, TFile, TGraphErrors, SetOwnership, TVector3
import math, sys, optparse, array, copy, os
import gc, inspect
import numpy as np

import include.Canvas as Canvas


################################# GLOBAL VARIABLES DEFINITION ####################################

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
    (opts, args) = parser.parse_args()


    ##################################
    ####   Variable declaration   ####
    ##################################
    MAX_DELTAR = 0.2 



    #################################
    ####   TEfficiency binning   ####
    #################################
    #Lxy_bin = np.array([0.0, 0.025, 0.5, 1.0, 2.0, 4.0, 8.0, 12.0, 16.0, 20., 30., 40., 50., 60., 70., 90., 110.0])
    #Lxy_bin = np.linspace(0.0, 110.0, 51)
    Lxy_bin = np.linspace(0.0, 110.0, 100)
    Lz_bin = np.linspace(0.0, 280.0, 100)
    Lxy_profbin = np.array([0.0, 1.0, 5.0, 10.0, 15.0, 20.0, 30.0, 40.0, 60.0, 80.0, 100.0])
    dxy_bin = np.linspace(0.0, 110.0, 100)
    dz_bin = np.linspace(0.0, 280.0, 100)
    Lxy_logbin = np.logspace(0.0, 3.0, 101)
    #pt_bin = np.concatenate((np.linspace(0, 125, 15), np.array([150, 175, 200, 250, 300, 400, 500])))
    pt_bin = np.linspace(0.0, 300.0, 80) # 100, 60 for DY
    eta_bin = np.linspace(-5.0, 5.0, 40)
    Lxy_sep = np.array([0.0, 1.0, 20.0, 60.0, 110.0])
    dxy_sep = np.array([0.0, 1.0, 20.0, 60.0, 110.0])
    Lz_sep = np.array([0.0, 1.0, 60.0, 120.0, 280.0])
    dz_sep = np.array([0.0, 1.0, 60.0, 120.0, 280.0])
    pt_sep = np.array([0.0, 50.0, 150.0, 300.0]) # supposed to end at infinity
    ptres_bin = np.linspace(-0.2, 0.2, 61)
    dxyres_bin = np.linspace(-0.1, 0.1, 61)
    

    ###############################
    ####   Book TH1F objects   ####
    ###############################
    
    #
    # -- genMu histograms
    #
    total_genMu_pt = r.TH1F("total_genMu_pt", ";Generated #mu p_{T} (GeV);Muons", len(pt_bin)-1, pt_bin)
    recoGM_genMu_pt = r.TH1F("recoGM_genMu_pt", ";Generated #mu p_{T} (GeV);Muons", len(pt_bin)-1, pt_bin)
    recoDG_genMu_pt = r.TH1F("recoDG_genMu_pt", ";Generated #mu p_{T} (GeV);Muons", len(pt_bin)-1, pt_bin)
    recoDGID_genMu_pt = r.TH1F("recoDGID_genMu_pt", ";Generated #mu p_{T} (GeV);Muons", len(pt_bin)-1, pt_bin)

    total_genMu_eta = r.TH1F("total_genMu_eta", ";Generated #mu #eta (GeV);Muons", len(eta_bin)-1, eta_bin)
    recoGM_genMu_eta = r.TH1F("recoGM_genMu_eta", ";Generated #mu #eta (GeV);Muons", len(eta_bin)-1, eta_bin)
    recoDG_genMu_eta = r.TH1F("recoDG_genMu_eta", ";Generated #mu #eta (GeV);Muons", len(eta_bin)-1, eta_bin)
    recoDGID_genMu_eta = r.TH1F("recoDGID_genMu_eta", ";Generated #mu #eta (GeV);Muons", len(eta_bin)-1, eta_bin)

    total_genMu_Lxy = r.TH1F("total_genMu_Lxy", ";Generated #mu decay L_{xy} (cm);Muons", len(Lxy_bin)-1, Lxy_bin)
    recoGM_genMu_Lxy = r.TH1F("recoGM_genMu_Lxy", ";Generated #mu decay L_{xy} (cm);Muons", len(Lxy_bin)-1, Lxy_bin)
    recoDG_genMu_Lxy = r.TH1F("recoDG_genMu_Lxy", ";Generated #mu decay L_{xy} (cm);Muons", len(Lxy_bin)-1, Lxy_bin)
    recoDGID_genMu_Lxy = r.TH1F("recoDGID_genMu_Lxy", ";Generated #mu decay L_{xy} (cm);Muons", len(Lxy_bin)-1, Lxy_bin)

    total_genMu_dxy = r.TH1F("total_genMu_dxy", ";Generated #mu decay |d_{xy}| (cm);Muons", len(dxy_bin)-1, dxy_bin)
    recoGM_genMu_dxy = r.TH1F("recoGM_genMu_dxy", ";Generated #mu decay |d_{xy}| (cm);Muons", len(dxy_bin)-1, dxy_bin)
    recoDG_genMu_dxy = r.TH1F("recoDG_genMu_dxy", ";Generated #mu decay |d_{xy}| (cm);Muons", len(dxy_bin)-1, dxy_bin)
    recoDGID_genMu_dxy = r.TH1F("recoDGID_genMu_dxy", ";Generated #mu decay |d_{xy}| (cm);Muons", len(dxy_bin)-1, dxy_bin)

    total_genMu_Lz = r.TH1F("total_genMu_Lz", ";Generated #mu decay L_{z} (cm);Muons", len(Lz_bin)-1, Lz_bin)
    recoGM_genMu_Lz = r.TH1F("recoGM_genMu_Lz", ";Generated #mu decay L_{z} (cm);Muons", len(Lz_bin)-1, Lz_bin)
    recoDG_genMu_Lz = r.TH1F("recoDG_genMu_Lz", ";Generated #mu decay L_{z} (cm);Muons", len(Lz_bin)-1, Lz_bin)
    recoDGID_genMu_Lz = r.TH1F("recoDGID_genMu_Lz", ";Generated #mu decay L_{z} (cm);Muons", len(Lz_bin)-1, Lz_bin)

    total_genMu_dz = r.TH1F("total_genMu_dz", ";Generated #mu decay |d_{z}| (cm);Muons", len(dz_bin)-1, dz_bin)
    recoGM_genMu_dz = r.TH1F("recoGM_genMu_dz", ";Generated #mu decay |d_{z}| (cm);Muons", len(dz_bin)-1, dz_bin)
    recoDG_genMu_dz = r.TH1F("recoDG_genMu_dz", ";Generated #mu decay |d_{z}| (cm);Muons", len(dz_bin)-1, dz_bin)
    recoDGID_genMu_dz = r.TH1F("recoDGID_genMu_dz", ";Generated #mu decay |d_{z}| (cm);Muons", len(dz_bin)-1, dz_bin)

    ######################################
    ####   Book TEfficiency objects   ####
    ######################################

    eff_GM_pt_Lxybin1 = r.TEfficiency("eff_GM_pt_Lxybin1", ";Generated muon p_{T} (GeV);Efficiency", len(pt_bin)-1, pt_bin)
    eff_GM_pt_Lxybin2 = r.TEfficiency("eff_GM_pt_Lxybin2", ";Generated muon p_{T} (GeV);Efficiency", len(pt_bin)-1, pt_bin)
    eff_GM_pt_Lxybin3 = r.TEfficiency("eff_GM_pt_Lxybin3", ";Generated muon p_{T} (GeV);Efficiency", len(pt_bin)-1, pt_bin)
    eff_GM_pt_Lxybin4 = r.TEfficiency("eff_GM_pt_Lxybin4", ";Generated muon p_{T} (GeV);Efficiency", len(pt_bin)-1, pt_bin)

    eff_DG_pt_Lxybin1 = r.TEfficiency("eff_DG_pt_Lxybin1", ";Generated muon p_{T} (GeV);Efficiency", len(pt_bin)-1, pt_bin)
    eff_DG_pt_Lxybin2 = r.TEfficiency("eff_DG_pt_Lxybin2", ";Generated muon p_{T} (GeV);Efficiency", len(pt_bin)-1, pt_bin)
    eff_DG_pt_Lxybin3 = r.TEfficiency("eff_DG_pt_Lxybin3", ";Generated muon p_{T} (GeV);Efficiency", len(pt_bin)-1, pt_bin)
    eff_DG_pt_Lxybin4 = r.TEfficiency("eff_DG_pt_Lxybin4", ";Generated muon p_{T} (GeV);Efficiency", len(pt_bin)-1, pt_bin)

    eff_DGID_pt_Lxybin1 = r.TEfficiency("eff_DGID_pt_Lxybin1", ";Generated muon p_{T} (GeV);Efficiency", len(pt_bin)-1, pt_bin)
    eff_DGID_pt_Lxybin2 = r.TEfficiency("eff_DGID_pt_Lxybin2", ";Generated muon p_{T} (GeV);Efficiency", len(pt_bin)-1, pt_bin)
    eff_DGID_pt_Lxybin3 = r.TEfficiency("eff_DGID_pt_Lxybin3", ";Generated muon p_{T} (GeV);Efficiency", len(pt_bin)-1, pt_bin)
    eff_DGID_pt_Lxybin4 = r.TEfficiency("eff_DGID_pt_Lxybin4", ";Generated muon p_{T} (GeV);Efficiency", len(pt_bin)-1, pt_bin)

    ######################################
    eff_GM_pt_dxybin1 = r.TEfficiency("eff_GM_pt_dxybin1", ";Generated muon p_{T} (GeV);Efficiency", len(pt_bin)-1, pt_bin)
    eff_GM_pt_dxybin2 = r.TEfficiency("eff_GM_pt_dxybin2", ";Generated muon p_{T} (GeV);Efficiency", len(pt_bin)-1, pt_bin)
    eff_GM_pt_dxybin3 = r.TEfficiency("eff_GM_pt_dxybin3", ";Generated muon p_{T} (GeV);Efficiency", len(pt_bin)-1, pt_bin)
    eff_GM_pt_dxybin4 = r.TEfficiency("eff_GM_pt_dxybin4", ";Generated muon p_{T} (GeV);Efficiency", len(pt_bin)-1, pt_bin)

    eff_DG_pt_dxybin1 = r.TEfficiency("eff_DG_pt_dxybin1", ";Generated muon p_{T} (GeV);Efficiency", len(pt_bin)-1, pt_bin)
    eff_DG_pt_dxybin2 = r.TEfficiency("eff_DG_pt_dxybin2", ";Generated muon p_{T} (GeV);Efficiency", len(pt_bin)-1, pt_bin)
    eff_DG_pt_dxybin3 = r.TEfficiency("eff_DG_pt_dxybin3", ";Generated muon p_{T} (GeV);Efficiency", len(pt_bin)-1, pt_bin)
    eff_DG_pt_dxybin4 = r.TEfficiency("eff_DG_pt_dxybin4", ";Generated muon p_{T} (GeV);Efficiency", len(pt_bin)-1, pt_bin)

    eff_DGID_pt_dxybin1 = r.TEfficiency("eff_DGID_pt_dxybin1", ";Generated muon p_{T} (GeV);Efficiency", len(pt_bin)-1, pt_bin)
    eff_DGID_pt_dxybin2 = r.TEfficiency("eff_DGID_pt_dxybin2", ";Generated muon p_{T} (GeV);Efficiency", len(pt_bin)-1, pt_bin)
    eff_DGID_pt_dxybin3 = r.TEfficiency("eff_DGID_pt_dxybin3", ";Generated muon p_{T} (GeV);Efficiency", len(pt_bin)-1, pt_bin)
    eff_DGID_pt_dxybin4 = r.TEfficiency("eff_DGID_pt_dxybin4", ";Generated muon p_{T} (GeV);Efficiency", len(pt_bin)-1, pt_bin)

    ###################################
    ####   Book Resolution TH1Fs   ####
    ###################################
    res_GM_pt = r.TH1F("res_GM_pt", ";(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{gen};Normalized muon yield", len(ptres_bin)-1, ptres_bin)
    res_GM_pt_Lxybin1 = r.TH1F("res_GM_pt_Lxybin1", ";(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{gen};Normalized muon yield", len(ptres_bin)-1, ptres_bin)
    res_GM_pt_Lxybin2 = r.TH1F("res_GM_pt_Lxybin2", ";(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{gen};Normalized muon yield", len(ptres_bin)-1, ptres_bin)
    res_GM_pt_Lxybin3 = r.TH1F("res_GM_pt_Lxybin3", ";(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{gen};Normalized muon yield", len(ptres_bin)-1, ptres_bin)
    res_GM_pt_Lxybin4 = r.TH1F("res_GM_pt_Lxybin4", ";(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{gen};Normalized muon yield", len(ptres_bin)-1, ptres_bin)
    res_GM_pt_dxybin1 = r.TH1F("res_GM_pt_dxybin1", ";(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{gen};Normalized muon yield", len(ptres_bin)-1, ptres_bin)
    res_GM_pt_dxybin2 = r.TH1F("res_GM_pt_dxybin2", ";(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{gen};Normalized muon yield", len(ptres_bin)-1, ptres_bin)
    res_GM_pt_dxybin3 = r.TH1F("res_GM_pt_dxybin3", ";(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{gen};Normalized muon yield", len(ptres_bin)-1, ptres_bin)
    res_GM_pt_dxybin4 = r.TH1F("res_GM_pt_dxybin4", ";(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{gen};Normalized muon yield", len(ptres_bin)-1, ptres_bin)
    res_GM_pt_ptbin1 = r.TH1F("res_GM_pt_ptbin1", ";(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{gen};Normalized muon yield", len(ptres_bin)-1, ptres_bin)
    res_GM_pt_ptbin2 = r.TH1F("res_GM_pt_ptbin2", ";(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{gen};Normalized muon yield", len(ptres_bin)-1, ptres_bin)
    res_GM_pt_ptbin3 = r.TH1F("res_GM_pt_ptbin3", ";(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{gen};Normalized muon yield", len(ptres_bin)-1, ptres_bin)
    res_GM_pt_ptbin4 = r.TH1F("res_GM_pt_ptbin4", ";(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{gen};Normalized muon yield", len(ptres_bin)-1, ptres_bin)


    res_DG_pt = r.TH1F("res_DG_pt", ";(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{gen};Normalized muon yield", len(ptres_bin)-1, ptres_bin)
    res_DG_pt_Lxybin1 = r.TH1F("res_DG_pt_Lxybin1", ";(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{gen};Normalized muon yield", len(ptres_bin)-1, ptres_bin)
    res_DG_pt_Lxybin2 = r.TH1F("res_DG_pt_Lxybin2", ";(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{gen};Normalized muon yield", len(ptres_bin)-1, ptres_bin)
    res_DG_pt_Lxybin3 = r.TH1F("res_DG_pt_Lxybin3", ";(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{gen};Normalized muon yield", len(ptres_bin)-1, ptres_bin)
    res_DG_pt_Lxybin4 = r.TH1F("res_DG_pt_Lxybin4", ";(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{gen};Normalized muon yield", len(ptres_bin)-1, ptres_bin)
    res_DG_pt_dxybin1 = r.TH1F("res_DG_pt_dxybin1", ";(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{gen};Normalized muon yield", len(ptres_bin)-1, ptres_bin)
    res_DG_pt_dxybin2 = r.TH1F("res_DG_pt_dxybin2", ";(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{gen};Normalized muon yield", len(ptres_bin)-1, ptres_bin)
    res_DG_pt_dxybin3 = r.TH1F("res_DG_pt_dxybin3", ";(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{gen};Normalized muon yield", len(ptres_bin)-1, ptres_bin)
    res_DG_pt_dxybin4 = r.TH1F("res_DG_pt_dxybin4", ";(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{gen};Normalized muon yield", len(ptres_bin)-1, ptres_bin)
    res_DG_pt_ptbin1 = r.TH1F("res_DG_pt_ptbin1", ";(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{gen};Normalized muon yield", len(ptres_bin)-1, ptres_bin)
    res_DG_pt_ptbin2 = r.TH1F("res_DG_pt_ptbin2", ";(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{gen};Normalized muon yield", len(ptres_bin)-1, ptres_bin)
    res_DG_pt_ptbin3 = r.TH1F("res_DG_pt_ptbin3", ";(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{gen};Normalized muon yield", len(ptres_bin)-1, ptres_bin)
    res_DG_pt_ptbin4 = r.TH1F("res_DG_pt_ptbin4", ";(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{gen};Normalized muon yield", len(ptres_bin)-1, ptres_bin)

    res_DGID_pt = r.TH1F("res_DGID_pt", ";(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{gen};Normalized muon yield", len(ptres_bin)-1, ptres_bin)
    res_DGID_pt_Lxybin1 = r.TH1F("res_DGID_pt_Lxybin1", ";(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{gen};Normalized muon yield", len(ptres_bin)-1, ptres_bin)
    res_DGID_pt_Lxybin2 = r.TH1F("res_DGID_pt_Lxybin2", ";(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{gen};Normalized muon yield", len(ptres_bin)-1, ptres_bin)
    res_DGID_pt_Lxybin3 = r.TH1F("res_DGID_pt_Lxybin3", ";(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{gen};Normalized muon yield", len(ptres_bin)-1, ptres_bin)
    res_DGID_pt_Lxybin4 = r.TH1F("res_DGID_pt_Lxybin4", ";(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{gen};Normalized muon yield", len(ptres_bin)-1, ptres_bin)
    res_DGID_pt_dxybin1 = r.TH1F("res_DGID_pt_dxybin1", ";(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{gen};Normalized muon yield", len(ptres_bin)-1, ptres_bin)
    res_DGID_pt_dxybin2 = r.TH1F("res_DGID_pt_dxybin2", ";(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{gen};Normalized muon yield", len(ptres_bin)-1, ptres_bin)
    res_DGID_pt_dxybin3 = r.TH1F("res_DGID_pt_dxybin3", ";(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{gen};Normalized muon yield", len(ptres_bin)-1, ptres_bin)
    res_DGID_pt_dxybin4 = r.TH1F("res_DGID_pt_dxybin4", ";(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{gen};Normalized muon yield", len(ptres_bin)-1, ptres_bin)
    res_DGID_pt_ptbin1 = r.TH1F("res_DGID_pt_ptbin1", ";(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{gen};Normalized muon yield", len(ptres_bin)-1, ptres_bin)
    res_DGID_pt_ptbin2 = r.TH1F("res_DGID_pt_ptbin2", ";(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{gen};Normalized muon yield", len(ptres_bin)-1, ptres_bin)
    res_DGID_pt_ptbin3 = r.TH1F("res_DGID_pt_ptbin3", ";(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{gen};Normalized muon yield", len(ptres_bin)-1, ptres_bin)
    res_DGID_pt_ptbin4 = r.TH1F("res_DGID_pt_ptbin4", ";(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{gen};Normalized muon yield", len(ptres_bin)-1, ptres_bin)

    res_GM_dxy = r.TH1F("res_GM_dxy", ";(d_{xy}^{reco} - d_{xy}^{gen})/d_{xy}^{gen};Normalized muon yield", len(dxyres_bin)-1, dxyres_bin)
    res_GM_dxy_Lxybin1 = r.TH1F("res_GM_dxy_Lxybin1", ";(d_{xy}^{reco} - d_{xy}^{gen})/d_{xy}^{gen};Normalized muon yield", len(dxyres_bin)-1, dxyres_bin)
    res_GM_dxy_Lxybin2 = r.TH1F("res_GM_dxy_Lxybin2", ";(d_{xy}^{reco} - d_{xy}^{gen})/d_{xy}^{gen};Normalized muon yield", len(dxyres_bin)-1, dxyres_bin)
    res_GM_dxy_Lxybin3 = r.TH1F("res_GM_dxy_Lxybin3", ";(d_{xy}^{reco} - d_{xy}^{gen})/d_{xy}^{gen};Normalized muon yield", len(dxyres_bin)-1, dxyres_bin)
    res_GM_dxy_Lxybin4 = r.TH1F("res_GM_dxy_Lxybin4", ";(d_{xy}^{reco} - d_{xy}^{gen})/d_{xy}^{gen};Normalized muon yield", len(dxyres_bin)-1, dxyres_bin)
    res_GM_dxy_dxybin1 = r.TH1F("res_GM_dxy_dxybin1", ";(d_{xy}^{reco} - d_{xy}^{gen})/d_{xy}^{gen};Normalized muon yield", len(dxyres_bin)-1, dxyres_bin)
    res_GM_dxy_dxybin2 = r.TH1F("res_GM_dxy_dxybin2", ";(d_{xy}^{reco} - d_{xy}^{gen})/d_{xy}^{gen};Normalized muon yield", len(dxyres_bin)-1, dxyres_bin)
    res_GM_dxy_dxybin3 = r.TH1F("res_GM_dxy_dxybin3", ";(d_{xy}^{reco} - d_{xy}^{gen})/d_{xy}^{gen};Normalized muon yield", len(dxyres_bin)-1, dxyres_bin)
    res_GM_dxy_dxybin4 = r.TH1F("res_GM_dxy_dxybin4", ";(d_{xy}^{reco} - d_{xy}^{gen})/d_{xy}^{gen};Normalized muon yield", len(dxyres_bin)-1, dxyres_bin)

    res_DG_dxy = r.TH1F("res_DG_dxy", ";(d_{xy}^{reco} - d_{xy}^{gen})/d_{xy}^{gen};Normalized muon yield", len(dxyres_bin)-1, dxyres_bin)
    res_DG_dxy_Lxybin1 = r.TH1F("res_DG_dxy_Lxybin1", ";(d_{xy}^{reco} - d_{xy}^{gen})/d_{xy}^{gen};Normalized muon yield", len(dxyres_bin)-1, dxyres_bin)
    res_DG_dxy_Lxybin2 = r.TH1F("res_DG_dxy_Lxybin2", ";(d_{xy}^{reco} - d_{xy}^{gen})/d_{xy}^{gen};Normalized muon yield", len(dxyres_bin)-1, dxyres_bin)
    res_DG_dxy_Lxybin3 = r.TH1F("res_DG_dxy_Lxybin3", ";(d_{xy}^{reco} - d_{xy}^{gen})/d_{xy}^{gen};Normalized muon yield", len(dxyres_bin)-1, dxyres_bin)
    res_DG_dxy_Lxybin4 = r.TH1F("res_DG_dxy_Lxybin4", ";(d_{xy}^{reco} - d_{xy}^{gen})/d_{xy}^{gen};Normalized muon yield", len(dxyres_bin)-1, dxyres_bin)
    res_DG_dxy_dxybin1 = r.TH1F("res_DG_dxy_dxybin1", ";(d_{xy}^{reco} - d_{xy}^{gen})/d_{xy}^{gen};Normalized muon yield", len(dxyres_bin)-1, dxyres_bin)
    res_DG_dxy_dxybin2 = r.TH1F("res_DG_dxy_dxybin2", ";(d_{xy}^{reco} - d_{xy}^{gen})/d_{xy}^{gen};Normalized muon yield", len(dxyres_bin)-1, dxyres_bin)
    res_DG_dxy_dxybin3 = r.TH1F("res_DG_dxy_dxybin3", ";(d_{xy}^{reco} - d_{xy}^{gen})/d_{xy}^{gen};Normalized muon yield", len(dxyres_bin)-1, dxyres_bin)
    res_DG_dxy_dxybin4 = r.TH1F("res_DG_dxy_dxybin4", ";(d_{xy}^{reco} - d_{xy}^{gen})/d_{xy}^{gen};Normalized muon yield", len(dxyres_bin)-1, dxyres_bin)

    res_DGID_dxy = r.TH1F("res_DGID_dxy", ";(d_{xy}^{reco} - d_{xy}^{gen})/d_{xy}^{gen};Normalized muon yield", len(dxyres_bin)-1, dxyres_bin)
    res_DGID_dxy_Lxybin1 = r.TH1F("res_DGID_dxy_Lxybin1", ";(d_{xy}^{reco} - d_{xy}^{gen})/d_{xy}^{gen};Normalized muon yield", len(dxyres_bin)-1, dxyres_bin)
    res_DGID_dxy_Lxybin2 = r.TH1F("res_DGID_dxy_Lxybin2", ";(d_{xy}^{reco} - d_{xy}^{gen})/d_{xy}^{gen};Normalized muon yield", len(dxyres_bin)-1, dxyres_bin)
    res_DGID_dxy_Lxybin3 = r.TH1F("res_DGID_dxy_Lxybin3", ";(d_{xy}^{reco} - d_{xy}^{gen})/d_{xy}^{gen};Normalized muon yield", len(dxyres_bin)-1, dxyres_bin)
    res_DGID_dxy_Lxybin4 = r.TH1F("res_DGID_dxy_Lxybin4", ";(d_{xy}^{reco} - d_{xy}^{gen})/d_{xy}^{gen};Normalized muon yield", len(dxyres_bin)-1, dxyres_bin)
    res_DGID_dxy_dxybin1 = r.TH1F("res_DGID_dxy_dxybin1", ";(d_{xy}^{reco} - d_{xy}^{gen})/d_{xy}^{gen};Normalized muon yield", len(dxyres_bin)-1, dxyres_bin)
    res_DGID_dxy_dxybin2 = r.TH1F("res_DGID_dxy_dxybin2", ";(d_{xy}^{reco} - d_{xy}^{gen})/d_{xy}^{gen};Normalized muon yield", len(dxyres_bin)-1, dxyres_bin)
    res_DGID_dxy_dxybin3 = r.TH1F("res_DGID_dxy_dxybin3", ";(d_{xy}^{reco} - d_{xy}^{gen})/d_{xy}^{gen};Normalized muon yield", len(dxyres_bin)-1, dxyres_bin)
    res_DGID_dxy_dxybin4 = r.TH1F("res_DGID_dxy_dxybin4", ";(d_{xy}^{reco} - d_{xy}^{gen})/d_{xy}^{gen};Normalized muon yield", len(dxyres_bin)-1, dxyres_bin)


    #########################
    ####   Load sample   ####
    #########################
    _sampleName = opts.filename
    _file = TFile(_sampleName)
    _tree = _file.Get("Events")
    print("TTree with " + str(_tree.GetEntries()) + " entries")


    ###################################
    ####   Loop over tree events   ####
    ###################################

    for i in range(0, _tree.GetEntries()):

        if i > opts.nmax and opts.nmax: break
        _tree.GetEntry(i)

        for j in range(0, _tree.ngenMu):

            if not _tree.genMu_isPromptFinalState[j]: continue

            pt    = _tree.genMu_pt[j]
            eta    = _tree.genMu_eta[j]
            phi    = _tree.genMu_phi[j]
            vx    = _tree.genMu_vx[j]
            vy    = _tree.genMu_vy[j]
            vz    = _tree.genMu_vz[j]
            dxy    = _tree.genMu_dxy[j]
            dxy_abs    = abs(dxy)
            dz    = _tree.genMu_dz[j]
            Lxy = math.sqrt(vx**2 + vy**2)
            Lz = math.sqrt(vz**2)

            if pt < 31: continue
            if abs(eta) > 2: continue

            l = TVector3()
            l.SetPtEtaPhi(pt, eta, phi)

            total_genMu_pt.Fill(pt)
            total_genMu_eta.Fill(eta)
            total_genMu_Lxy.Fill(Lxy)
            total_genMu_Lz.Fill(Lz)
            total_genMu_dxy.Fill(dxy_abs)
            total_genMu_dz.Fill(dz)

            #
            # -- GBs
            #
            deltaR = 9999.0
            index = -9
            for k in range(0, _tree.nGM):
                if _tree.GM_pt[k] < 31: continue
                if abs(_tree.GM_eta[k]) > 2: continue
                re = TVector3()
                re.SetPtEtaPhi(_tree.GM_pt[k], _tree.GM_eta[k], _tree.GM_phi[k])
                if l.DeltaR(re) < deltaR:
                    deltaR = l.DeltaR(re)
                    index = k

            if deltaR < MAX_DELTAR:

                ptres = (_tree.GM_pt[index] - pt)/pt
                dxyres = (_tree.GM_dxy[index] + dxy)/dxy_abs

                recoGM_genMu_pt.Fill(pt)
                recoGM_genMu_eta.Fill(eta)
                recoGM_genMu_Lxy.Fill(Lxy)
                recoGM_genMu_Lz.Fill(Lz)
                recoGM_genMu_dxy.Fill(dxy_abs)
                recoGM_genMu_dz.Fill(dz)

                res_GM_pt.Fill(ptres)
                res_GM_dxy.Fill(dxyres)

                # Lxy bins
                if Lxy < Lxy_sep[1]:
                    res_GM_pt_Lxybin1.Fill(ptres)
                    res_GM_dxy_Lxybin1.Fill(dxyres)
                    eff_GM_pt_Lxybin1.Fill(True, pt)
                elif Lxy > Lxy_sep[1] and Lxy < Lxy_sep[2]:
                    res_GM_pt_Lxybin2.Fill(ptres)
                    res_GM_dxy_Lxybin2.Fill(dxyres)
                    eff_GM_pt_Lxybin2.Fill(True, pt)
                elif Lxy > Lxy_sep[2] and Lxy < Lxy_sep[3]:
                    res_GM_pt_Lxybin3.Fill(ptres)
                    res_GM_dxy_Lxybin3.Fill(dxyres)
                    eff_GM_pt_Lxybin3.Fill(True, pt)
                elif Lxy > Lxy_sep[3] and Lxy < Lxy_sep[4]:
                    res_GM_pt_Lxybin4.Fill(ptres)
                    res_GM_dxy_Lxybin4.Fill(dxyres)
                    eff_GM_pt_Lxybin4.Fill(True, pt)

                # dxy bins
                if dxy_abs < dxy_sep[1]:
                    res_GM_pt_dxybin1.Fill(ptres)
                    res_GM_dxy_dxybin1.Fill(dxyres)
                    eff_GM_pt_dxybin1.Fill(True, pt)
                elif dxy_abs > dxy_sep[1] and dxy_abs < dxy_sep[2]:
                    res_GM_pt_dxybin2.Fill(ptres)
                    res_GM_dxy_dxybin2.Fill(dxyres)
                    eff_GM_pt_dxybin2.Fill(True, pt)
                elif dxy_abs > dxy_sep[2] and dxy_abs < dxy_sep[3]:
                    res_GM_pt_dxybin3.Fill(ptres)
                    res_GM_dxy_dxybin3.Fill(dxyres)
                    eff_GM_pt_dxybin3.Fill(True, pt)
                elif dxy_abs > dxy_sep[3] and dxy_abs < dxy_sep[4]:
                    res_GM_pt_dxybin4.Fill(ptres)
                    res_GM_dxy_dxybin4.Fill(dxyres)
                    eff_GM_pt_dxybin4.Fill(True, pt)

                # pt bins
                if pt < pt_sep[1]:
                    res_GM_pt_ptbin1.Fill(ptres)
                elif pt > pt_sep[1] and pt < pt_sep[2]:
                    res_GM_pt_ptbin2.Fill(ptres)
                elif pt > pt_sep[2] and pt < pt_sep[3]:
                    res_GM_pt_ptbin3.Fill(ptres)
                elif pt > pt_sep[3]:
                    res_GM_pt_ptbin4.Fill(ptres)

            else:

                if Lxy < Lxy_sep[1]:
                    eff_GM_pt_Lxybin1.Fill(False, pt)
                elif Lxy > Lxy_sep[1] and Lxy < Lxy_sep[2]:
                    eff_GM_pt_Lxybin2.Fill(False, pt)
                elif Lxy > Lxy_sep[2] and Lxy < Lxy_sep[3]:
                    eff_GM_pt_Lxybin3.Fill(False, pt)
                elif Lxy > Lxy_sep[3] and Lxy < Lxy_sep[4]:
                    eff_GM_pt_Lxybin4.Fill(False, pt)


                if dxy_abs < dxy_sep[1]:
                    eff_GM_pt_dxybin1.Fill(False, pt)
                elif dxy_abs > dxy_sep[1] and dxy_abs < dxy_sep[2]:
                    eff_GM_pt_dxybin2.Fill(False, pt)
                elif dxy_abs > dxy_sep[2] and dxy_abs < dxy_sep[3]:
                    eff_GM_pt_dxybin3.Fill(False, pt)
                elif dxy_abs > dxy_sep[3] and dxy_abs < dxy_sep[4]:
                    eff_GM_pt_dxybin4.Fill(False, pt)


            #
            # -- DGs
            #
            deltaR = 9999.0
            index = -9
            for k in range(0, _tree.nDG):
                if _tree.DG_pt[k] < 31: continue
                if abs(_tree.DG_eta[k]) > 2: continue
                re = TVector3()
                re.SetPtEtaPhi(_tree.DG_pt[k], _tree.DG_eta[k], _tree.DG_phi[k])
                if l.DeltaR(re) < deltaR:
                    deltaR = l.DeltaR(re)
                    index = k

            

            if deltaR < MAX_DELTAR:

                ptres = (_tree.DG_pt[index] - pt)/pt
                dxyres = (_tree.DG_dxy[index] + dxy)/dxy_abs

                recoDG_genMu_pt.Fill(pt)
                recoDG_genMu_eta.Fill(eta)
                recoDG_genMu_Lxy.Fill(Lxy)
                recoDG_genMu_Lz.Fill(Lz)
                recoDG_genMu_dxy.Fill(dxy_abs)
                recoDG_genMu_dz.Fill(dz)

                res_DG_pt.Fill(ptres)
                res_DG_dxy.Fill(dxyres)


                if Lxy < Lxy_sep[1]:
                    res_DG_pt_Lxybin1.Fill(ptres)
                    res_DG_dxy_Lxybin1.Fill(dxyres)
                    eff_DG_pt_Lxybin1.Fill(True, pt)
                elif Lxy > Lxy_sep[1] and Lxy < Lxy_sep[2]:
                    res_DG_pt_Lxybin2.Fill(ptres)
                    res_DG_dxy_Lxybin2.Fill(dxyres)
                    eff_DG_pt_Lxybin2.Fill(True, pt)
                elif Lxy > Lxy_sep[2] and Lxy < Lxy_sep[3]:
                    res_DG_pt_Lxybin3.Fill(ptres)
                    res_DG_dxy_Lxybin3.Fill(dxyres)
                    eff_DG_pt_Lxybin3.Fill(True, pt)
                elif Lxy > Lxy_sep[3] and Lxy < Lxy_sep[4]:
                    res_DG_pt_Lxybin4.Fill(ptres)
                    res_DG_dxy_Lxybin4.Fill(dxyres)
                    eff_DG_pt_Lxybin4.Fill(True, pt)

                if dxy_abs < dxy_sep[1]:
                    res_DG_pt_dxybin1.Fill(ptres)
                    res_DG_dxy_dxybin1.Fill(dxyres)
                    eff_DG_pt_dxybin1.Fill(True, pt)
                elif dxy_abs > dxy_sep[1] and dxy_abs < dxy_sep[2]:
                    res_DG_pt_dxybin2.Fill(ptres)
                    res_DG_dxy_dxybin2.Fill(dxyres)
                    eff_DG_pt_dxybin2.Fill(True, pt)
                elif dxy_abs > dxy_sep[2] and dxy_abs < dxy_sep[3]:
                    res_DG_pt_dxybin3.Fill(ptres)
                    res_DG_dxy_dxybin3.Fill(dxyres)
                    eff_DG_pt_dxybin3.Fill(True, pt)
                elif dxy_abs > dxy_sep[3] and dxy_abs < dxy_sep[4]:
                    res_DG_pt_dxybin4.Fill(ptres)
                    res_DG_dxy_dxybin4.Fill(dxyres)
                    eff_DG_pt_dxybin4.Fill(True, pt)

                # pt bins
                if pt < pt_sep[1]:
                    res_DG_pt_ptbin1.Fill(ptres)
                elif pt > pt_sep[1] and pt < pt_sep[2]:
                    res_DG_pt_ptbin2.Fill(ptres)
                elif pt > pt_sep[2] and pt < pt_sep[3]:
                    res_DG_pt_ptbin3.Fill(ptres)
                elif pt > pt_sep[3]:
                    res_DG_pt_ptbin4.Fill(ptres)

            else:

                if Lxy < Lxy_sep[1]:
                    eff_DG_pt_Lxybin1.Fill(False, pt)
                elif Lxy > Lxy_sep[1] and Lxy < Lxy_sep[2]:
                    eff_DG_pt_Lxybin2.Fill(False, pt)
                elif Lxy > Lxy_sep[2] and Lxy < Lxy_sep[3]:
                    eff_DG_pt_Lxybin3.Fill(False, pt)
                elif Lxy > Lxy_sep[3] and Lxy < Lxy_sep[4]:
                    eff_DG_pt_Lxybin4.Fill(False, pt)

                if dxy_abs < dxy_sep[1]:
                    eff_DG_pt_dxybin1.Fill(False, pt)
                elif dxy_abs > dxy_sep[1] and dxy_abs < dxy_sep[2]:
                    eff_DG_pt_dxybin2.Fill(False, pt)
                elif dxy_abs > dxy_sep[2] and dxy_abs < dxy_sep[3]:
                    eff_DG_pt_dxybin3.Fill(False, pt)
                elif dxy_abs > dxy_sep[3] and dxy_abs < dxy_sep[4]:
                    eff_DG_pt_dxybin4.Fill(False, pt)

            #
            # -- DGs (+ID)
            #
            deltaR = 9999.0
            index = -9
            for k in range(0, _tree.nDG):
                #print(_tree.DG_pt[k], _tree.DG_ptError[k]/_tree.DG_pt[k], _tree.DG_normChi2[k], _tree.DG_numberOfValidHits[k])
                if _tree.DG_pt[k] < 31: continue
                if abs(_tree.DG_eta[k]) > 2: continue
                if _tree.DG_pt[k] < 31: continue
                if _tree.DG_ptError[k]/_tree.DG_pt[k] > 0.3: continue
                if _tree.DG_normChi2[k] > 10: continue
                if _tree.DG_numberOfValidHits[k] < 22: continue
                if abs(_tree.DG_eta[k]) > 2: continue
                re = TVector3()
                re.SetPtEtaPhi(_tree.DG_pt[k], _tree.DG_eta[k], _tree.DG_phi[k])
                if l.DeltaR(re) < deltaR:
                    deltaR = l.DeltaR(re)
                    index = k


            if deltaR < MAX_DELTAR:

                ptres = (_tree.DG_pt[index] - pt)/pt
                dxyres = (_tree.DG_dxy[index] + dxy)/dxy_abs

                 
                recoDGID_genMu_pt.Fill(pt)
                recoDGID_genMu_eta.Fill(eta)
                recoDGID_genMu_Lxy.Fill(Lxy)
                recoDGID_genMu_Lz.Fill(Lz)
                recoDGID_genMu_dxy.Fill(dxy_abs)
                recoDGID_genMu_dz.Fill(dz)
                

                res_DGID_pt.Fill(ptres)
                res_DGID_dxy.Fill(dxyres)
               

                if Lxy < Lxy_sep[1]:
                    res_DGID_pt_Lxybin1.Fill(ptres)
                    res_DGID_dxy_Lxybin1.Fill(dxyres)
                    eff_DGID_pt_Lxybin1.Fill(True, pt)
                elif Lxy > Lxy_sep[1] and Lxy < Lxy_sep[2]:
                    res_DGID_pt_Lxybin2.Fill(ptres)
                    res_DGID_dxy_Lxybin2.Fill(dxyres)
                    eff_DGID_pt_Lxybin2.Fill(True, pt)
                elif Lxy > Lxy_sep[2] and Lxy < Lxy_sep[3]:
                    res_DGID_pt_Lxybin3.Fill(ptres)
                    res_DGID_dxy_Lxybin3.Fill(dxyres)
                    eff_DGID_pt_Lxybin3.Fill(True, pt)
                elif Lxy > Lxy_sep[3] and Lxy < Lxy_sep[4]:
                    res_DGID_pt_Lxybin4.Fill(ptres)
                    res_DGID_dxy_Lxybin4.Fill(dxyres)
                    eff_DGID_pt_Lxybin4.Fill(True, pt)

                if dxy_abs < dxy_sep[1]:
                    res_DGID_pt_dxybin1.Fill(ptres)
                    res_DGID_dxy_dxybin1.Fill(dxyres)
                    eff_DGID_pt_dxybin1.Fill(True, pt)
                elif dxy_abs > dxy_sep[1] and dxy_abs < dxy_sep[2]:
                    res_DGID_pt_dxybin2.Fill(ptres)
                    res_DGID_dxy_dxybin2.Fill(dxyres)
                    eff_DGID_pt_dxybin2.Fill(True, pt)
                elif dxy_abs > dxy_sep[2] and dxy_abs < dxy_sep[3]:
                    res_DGID_pt_dxybin3.Fill(ptres)
                    res_DGID_dxy_dxybin3.Fill(dxyres)
                    eff_DGID_pt_dxybin3.Fill(True, pt)
                elif dxy_abs > dxy_sep[3] and dxy_abs < dxy_sep[4]:
                    res_DGID_pt_dxybin4.Fill(ptres)
                    res_DGID_dxy_dxybin4.Fill(dxyres)
                    eff_DGID_pt_dxybin4.Fill(True, pt)

                # pt bins
                if pt < pt_sep[1]:
                    res_DGID_pt_ptbin1.Fill(ptres)
                elif pt > pt_sep[1] and pt < pt_sep[2]:
                    res_DGID_pt_ptbin2.Fill(ptres)
                elif pt > pt_sep[2] and pt < pt_sep[3]:
                    res_DGID_pt_ptbin3.Fill(ptres)
                elif pt > pt_sep[3]:
                    res_DGID_pt_ptbin4.Fill(ptres)

            else:

                if Lxy < Lxy_sep[1]:
                    eff_DGID_pt_Lxybin1.Fill(False, pt)
                elif Lxy > Lxy_sep[1] and Lxy < Lxy_sep[2]:
                    eff_DGID_pt_Lxybin2.Fill(False, pt)
                elif Lxy > Lxy_sep[2] and Lxy < Lxy_sep[3]:
                    eff_DGID_pt_Lxybin3.Fill(False, pt)
                elif Lxy > Lxy_sep[3] and Lxy < Lxy_sep[4]:
                    eff_DGID_pt_Lxybin4.Fill(False, pt)

                if dxy_abs < dxy_sep[1]:
                    eff_DGID_pt_dxybin1.Fill(False, pt)
                elif dxy_abs > dxy_sep[1] and dxy_abs < dxy_sep[2]:
                    eff_DGID_pt_dxybin2.Fill(False, pt)
                elif dxy_abs > dxy_sep[2] and dxy_abs < dxy_sep[3]:
                    eff_DGID_pt_dxybin3.Fill(False, pt)
                elif dxy_abs > dxy_sep[3] and dxy_abs < dxy_sep[4]:
                    eff_DGID_pt_dxybin4.Fill(False, pt)
              


    #####################################
    ####   Construct TEfficiencies   ####
    #####################################
    eff_GM_pt = r.TEfficiency(recoGM_genMu_pt, total_genMu_pt)
    eff_GM_pt.SetTitle('eff_GM_pt;'+total_genMu_pt.GetXaxis().GetTitle()+'; Efficiency')
    eff_GM_eta = r.TEfficiency(recoGM_genMu_eta, total_genMu_eta)
    eff_GM_eta.SetTitle('eff_GM_eta;'+total_genMu_eta.GetXaxis().GetTitle()+'; Efficiency')
    eff_GM_Lxy = r.TEfficiency(recoGM_genMu_Lxy, total_genMu_Lxy)
    eff_GM_Lxy.SetTitle('eff_GM_Lxy;'+total_genMu_Lxy.GetXaxis().GetTitle()+'; Efficiency')
    eff_GM_Lz = r.TEfficiency(recoGM_genMu_Lz, total_genMu_Lz)
    eff_GM_Lz.SetTitle('eff_GM_Lz;'+total_genMu_Lz.GetXaxis().GetTitle()+'; Efficiency')
    eff_GM_dxy = r.TEfficiency(recoGM_genMu_dxy, total_genMu_dxy)
    eff_GM_dxy.SetTitle('eff_GM_dxy;'+total_genMu_dxy.GetXaxis().GetTitle()+'; Efficiency')
    eff_GM_dz = r.TEfficiency(recoGM_genMu_dz, total_genMu_dz)
    eff_GM_dz.SetTitle('eff_GM_dz;'+total_genMu_dz.GetXaxis().GetTitle()+'; Efficiency')

    eff_DG_pt = r.TEfficiency(recoDG_genMu_pt, total_genMu_pt)
    eff_DG_pt.SetTitle('eff_DG_pt;'+total_genMu_pt.GetXaxis().GetTitle()+'; Efficiency')
    eff_DG_eta = r.TEfficiency(recoDG_genMu_eta, total_genMu_eta)
    eff_DG_eta.SetTitle('eff_DG_eta;'+total_genMu_eta.GetXaxis().GetTitle()+'; Efficiency')
    eff_DG_Lxy = r.TEfficiency(recoDG_genMu_Lxy, total_genMu_Lxy)
    eff_DG_Lxy.SetTitle('eff_DG_Lxy;'+total_genMu_Lxy.GetXaxis().GetTitle()+'; Efficiency')
    eff_DG_Lz = r.TEfficiency(recoDG_genMu_Lz, total_genMu_Lz)
    eff_DG_Lz.SetTitle('eff_DG_Lz;'+total_genMu_Lz.GetXaxis().GetTitle()+'; Efficiency')
    eff_DG_dxy = r.TEfficiency(recoDG_genMu_dxy, total_genMu_dxy)
    eff_DG_dxy.SetTitle('eff_DG_dxy;'+total_genMu_dxy.GetXaxis().GetTitle()+'; Efficiency')
    eff_DG_dz = r.TEfficiency(recoDG_genMu_dz, total_genMu_dz)
    eff_DG_dz.SetTitle('eff_DG_dz;'+total_genMu_dz.GetXaxis().GetTitle()+'; Efficiency')

    eff_DGID_pt = r.TEfficiency(recoDGID_genMu_pt, total_genMu_pt)
    eff_DGID_pt.SetTitle('eff_DGID_pt;'+total_genMu_pt.GetXaxis().GetTitle()+'; Efficiency')
    eff_DGID_eta = r.TEfficiency(recoDGID_genMu_eta, total_genMu_eta)
    eff_DGID_eta.SetTitle('eff_DGID_eta;'+total_genMu_eta.GetXaxis().GetTitle()+'; Efficiency')
    eff_DGID_Lxy = r.TEfficiency(recoDGID_genMu_Lxy, total_genMu_Lxy)
    eff_DGID_Lxy.SetTitle('eff_DGID_Lxy;'+total_genMu_Lxy.GetXaxis().GetTitle()+'; Efficiency')
    eff_DGID_Lz = r.TEfficiency(recoDGID_genMu_Lz, total_genMu_Lz)
    eff_DGID_Lz.SetTitle('eff_DGID_Lz;'+total_genMu_Lz.GetXaxis().GetTitle()+'; Efficiency')
    eff_DGID_dxy = r.TEfficiency(recoDGID_genMu_dxy, total_genMu_dxy)
    eff_DGID_dxy.SetTitle('eff_DGID_dxy;'+total_genMu_dxy.GetXaxis().GetTitle()+'; Efficiency')
    eff_DGID_dz = r.TEfficiency(recoDGID_genMu_dz, total_genMu_dz)
    eff_DGID_dz.SetTitle('eff_DGID_dz;'+total_genMu_dz.GetXaxis().GetTitle()+'; Efficiency')

    if not os.path.exists(WORKPATH + 'plots_'+opts.tag+'/'): os.makedirs(WORKPATH + 'plots_'+opts.tag+'/')
    outputFile = TFile(WORKPATH +'plots_'+ opts.tag + '/th1fs.root', 'RECREATE')



    #### Write everything to use later:
    total_genMu_pt.Write()
    recoGM_genMu_pt.Write()
    recoDG_genMu_pt.Write()
    recoDGID_genMu_pt.Write()
    eff_GM_pt.Write()
    eff_DG_pt.Write()
    eff_DGID_pt.Write()
    eff_GM_pt_Lxybin1.Write()
    eff_GM_pt_Lxybin2.Write()
    eff_GM_pt_Lxybin3.Write()
    eff_GM_pt_Lxybin4.Write()
    eff_DG_pt_Lxybin1.Write()
    eff_DG_pt_Lxybin2.Write()
    eff_DG_pt_Lxybin3.Write()
    eff_DG_pt_Lxybin4.Write()
    eff_DGID_pt_Lxybin1.Write()
    eff_DGID_pt_Lxybin2.Write()
    eff_DGID_pt_Lxybin3.Write()
    eff_DGID_pt_Lxybin4.Write()
    eff_GM_pt_dxybin1.Write()
    eff_GM_pt_dxybin2.Write()
    eff_GM_pt_dxybin3.Write()
    eff_GM_pt_dxybin4.Write()
    eff_DG_pt_dxybin1.Write()
    eff_DG_pt_dxybin2.Write()
    eff_DG_pt_dxybin3.Write()
    eff_DG_pt_dxybin4.Write()
    eff_DGID_pt_dxybin1.Write()
    eff_DGID_pt_dxybin2.Write()
    eff_DGID_pt_dxybin3.Write()
    eff_DGID_pt_dxybin4.Write()

    total_genMu_eta.Write()
    recoGM_genMu_eta.Write()
    recoDG_genMu_eta.Write()
    recoDGID_genMu_eta.Write()
    eff_GM_eta.Write()
    eff_DG_eta.Write()
    eff_DGID_eta.Write()

    total_genMu_Lxy.Write()
    recoGM_genMu_Lxy.Write()
    recoDG_genMu_Lxy.Write()
    recoDGID_genMu_Lxy.Write()
    eff_GM_Lxy.Write()
    eff_DG_Lxy.Write()
    eff_DGID_Lxy.Write()

    total_genMu_Lz.Write()
    recoGM_genMu_Lz.Write()
    recoDG_genMu_Lz.Write()
    recoDGID_genMu_Lz.Write()
    eff_GM_Lz.Write()
    eff_DG_Lz.Write()
    eff_DGID_Lz.Write()

    total_genMu_dxy.Write()
    recoGM_genMu_dxy.Write()
    recoDG_genMu_dxy.Write()
    recoDGID_genMu_dxy.Write()
    eff_GM_dxy.Write()
    eff_DG_dxy.Write()
    eff_DGID_dxy.Write()

    total_genMu_dz.Write()
    recoGM_genMu_dz.Write()
    recoDG_genMu_dz.Write()
    recoDGID_genMu_dz.Write()
    eff_GM_dz.Write()
    eff_DG_dz.Write()
    eff_DGID_dz.Write()

    res_GM_pt.Write()
    res_GM_pt_Lxybin1.Write()
    res_GM_pt_Lxybin2.Write()
    res_GM_pt_Lxybin3.Write()
    res_GM_pt_Lxybin4.Write()
    res_GM_pt_dxybin1.Write()
    res_GM_pt_dxybin2.Write()
    res_GM_pt_dxybin3.Write()
    res_GM_pt_dxybin4.Write()
    res_GM_pt_ptbin1.Write()
    res_GM_pt_ptbin2.Write()
    res_GM_pt_ptbin3.Write()
    res_GM_pt_ptbin4.Write()

    res_DG_pt.Write()
    res_DG_pt_Lxybin1.Write()
    res_DG_pt_Lxybin2.Write()
    res_DG_pt_Lxybin3.Write()
    res_DG_pt_Lxybin4.Write()
    res_DG_pt_dxybin1.Write()
    res_DG_pt_dxybin2.Write()
    res_DG_pt_dxybin3.Write()
    res_DG_pt_dxybin4.Write()
    res_DG_pt_ptbin1.Write()
    res_DG_pt_ptbin2.Write()
    res_DG_pt_ptbin3.Write()
    res_DG_pt_ptbin4.Write()

    res_DGID_pt.Write()
    res_DGID_pt_Lxybin1.Write()
    res_DGID_pt_Lxybin2.Write()
    res_DGID_pt_Lxybin3.Write()
    res_DGID_pt_Lxybin4.Write()
    res_DGID_pt_dxybin1.Write()
    res_DGID_pt_dxybin2.Write()
    res_DGID_pt_dxybin3.Write()
    res_DGID_pt_dxybin4.Write()
    res_DGID_pt_ptbin1.Write()
    res_DGID_pt_ptbin2.Write()
    res_DGID_pt_ptbin3.Write()
    res_DGID_pt_ptbin4.Write()

    res_GM_dxy.Write()
    res_GM_dxy_Lxybin1.Write()
    res_GM_dxy_Lxybin2.Write()
    res_GM_dxy_Lxybin3.Write()
    res_GM_dxy_Lxybin4.Write()
    res_GM_dxy_dxybin1.Write()
    res_GM_dxy_dxybin2.Write()
    res_GM_dxy_dxybin3.Write()
    res_GM_dxy_dxybin4.Write()

    res_DG_dxy.Write()
    res_DG_dxy_Lxybin1.Write()
    res_DG_dxy_Lxybin2.Write()
    res_DG_dxy_Lxybin3.Write()
    res_DG_dxy_Lxybin4.Write()
    res_DG_dxy_dxybin1.Write()
    res_DG_dxy_dxybin2.Write()
    res_DG_dxy_dxybin3.Write()
    res_DG_dxy_dxybin4.Write()

    res_DGID_dxy.Write()
    res_DGID_dxy_Lxybin1.Write()
    res_DGID_dxy_Lxybin2.Write()
    res_DGID_dxy_Lxybin3.Write()
    res_DGID_dxy_Lxybin4.Write()
    res_DGID_dxy_dxybin1.Write()
    res_DGID_dxy_dxybin2.Write()
    res_DGID_dxy_dxybin3.Write()
    res_DGID_dxy_dxybin4.Write()

    outputFile.Close()

