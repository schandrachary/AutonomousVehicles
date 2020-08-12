#include "kalman_filter.h"
#include <cmath>
#include <iostream>

using Eigen::MatrixXd;
using Eigen::VectorXd;

/*
 * Please note that the Eigen library does not initialize
 *   VectorXd or MatrixXd objects with zeros upon creation.
 */

KalmanFilter::KalmanFilter() {}

KalmanFilter::~KalmanFilter() {}

void KalmanFilter::Init(VectorXd &x_in, MatrixXd &P_in, MatrixXd &F_in,
                        MatrixXd &H_in, MatrixXd &R_in, MatrixXd &Q_in) {
  x_ = x_in;
  P_ = P_in;
  F_ = F_in;
  H_ = H_in;
  R_ = R_in;
  Q_ = Q_in;
}

void KalmanFilter::Predict() {
  /**
   * predict the state
   */

   x_ = F_ * x_;
   P_ = F_ * P_ * F_.transpose() + Q_;
}

void KalmanFilter::Update(const VectorXd &z) {
  /**
   * update the state by using Kalman Filter equations
   */
   VectorXd z_pred = H_ * x_;
   VectorXd y = z - z_pred;
   MatrixXd Ht = H_.transpose();
   MatrixXd S = H_ * P_ * Ht + R_;
   MatrixXd Si = S.inverse();
   MatrixXd PHt = P_ * Ht;
   MatrixXd K = PHt * Si;

   // New estimate
   x_ = x_ + (K * y);
   long x_size = x_.size();
   MatrixXd I = MatrixXd::Identity(x_size, x_size);
   P_ = (I - K * H_) * P_;
}

void KalmanFilter::UpdateEKF(const VectorXd &z) {
  /**
   * update the state by using Extended Kalman Filter equations
   */
   float px = x_(0);
   float py = x_(1);
   float vx = x_(2);
   float vy = x_(3);

   float c1 = std::sqrt(px*px + py*py);
   float c2 = px*vx + py*vy;
   MatrixXd Hj = tools.CalculateJacobian(x_);

   VectorXd hx(3);
   hx(0) = c1;
   hx(1) = atan2(py,px);
   hx(2) = c2/c1;

   VectorXd y = z - hx;

   float phi = y(1);
   if(phi > M_PI || phi < -M_PI)
   {
     phi = atan2(sin(phi), cos(phi));
     y(1) = phi;
   }

   MatrixXd Hj_t = Hj.transpose();
   MatrixXd S = Hj * P_ * Hj_t + R_;
   MatrixXd Si = S.inverse();
   MatrixXd PHt = P_ * Hj_t;
   MatrixXd K = PHt * Si;

   // New estimate
   x_ = x_ + (K * y);
   long x_size = x_.size();
   MatrixXd I = MatrixXd::Identity(x_size, x_size);
   P_ = (I - K * Hj) * P_;
}
