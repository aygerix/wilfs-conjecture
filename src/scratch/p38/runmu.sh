#!/bin/bash
# MU-LO / Qa adversarial annealing (q5annMU): OBJM maximizes (mu*hlo_mu + h_hi)/Delta3 over mu <= e; OBJQ minimizes Qa.
# Calibration: exhaustive max MU-LO ratio 0.387 (e = 7), 0.366 (e = 8); exhaustive min Qa 4 (e = 7, 8).
cd ~/wilf/p38
( OBJM=1 ./q5annMU 6 20 60 100 6000 6601 > mu_M_d6.txt; echo "M d6 exit $?" ) &
( OBJM=1 ./q5annMU 7 25 80 100 6000 6701 > mu_M_d7.txt; echo "M d7 exit $?" ) &
( OBJM=1 ./q5annMU 8 35 115 100 6000 6801 > mu_M_d8.txt; echo "M d8 exit $?" ) &
( OBJM=1 ./q5annMU 9 40 150 100 6000 6901 > mu_M_d9.txt; echo "M d9 exit $?" ) &
( OBJM=1 ./q5annMU 11 50 200 100 6000 61101 > mu_M_d11.txt; echo "M d11 exit $?" ) &
( OBJQ=1 ./q5annMU 7 25 80 100 6000 7701 > mu_Q_d7.txt; echo "Q d7 exit $?" ) &
( OBJQ=1 ./q5annMU 9 40 150 100 6000 7901 > mu_Q_d9.txt; echo "Q d9 exit $?" ) &
( OBJQ=1 MU=3 BLO=40 ./q5annMU 9 40 150 100 6000 7931 > mu_Q3_d9.txt; echo "Q3 d9 exit $?" ) &
wait
echo DONE $(date)
