# Ozone-and-SOA-Formation-Potential
This repository contains documents and scripts to estimate Ozone and Secondary Organic Aerosol Formation Potential.
The estimation is performed from the source contributions obtained from PMF source apportionment. You will also need the input database used in the PMF analysis. 

Ozone formation potential of VOC sources
With the complex role of VOCs in facilitating tropospheric ozone formation, the ozone formation potential (OFP) of VOC sources were estimated following the method proposed by Carter (1994) using Eq. 1: 

〖OFP〗_i  = 〖MIR〗_i  × 〖VOC〗_i (Eq. 1)

where VOCi is the PMF residual-corrected concentration of VOC species i (unit: ppbv) and MIRi is the maximum incremental reactivity coefficient (unit: ppbv O3 / ppbv VOC) for each individual specie i. The PMF-resolved percentage contribution by specie on each source was used to estimate the source contributions to ozone formation. This was performed separately for the OCDN and ICDN datasets. 

Secondary organic aerosol formation potential of VOC sources
Secondary organic aerosol (SOA) formation was also estimated using the relative propensities of each specie for SOA formation relative to toluene following the method proposed by Derwent et al. (2010) using Eq. 2: 

〖SOAP〗_i  = P_i  × 〖VOC〗_i (Eq. 2)

where VOCi is the PMF residual-corrected concentration of VOC species i (unit: ppbv) and Pi is the relative propensity coefficient (arbitrary units) for each individual specie i. The PMF-resolved percentage contribution by specie on each source was used to estimate the source contributions to SOA formation. This was performed separately for the OCDN and ICDN datasets.


