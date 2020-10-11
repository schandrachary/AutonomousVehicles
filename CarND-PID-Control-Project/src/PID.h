#ifndef PID_H
#define PID_H

#include <array>

using std::vector;

class PID {
 public:
  /**
   * Constructor
   */
  PID();

  /**
   * Destructor.
   */
  virtual ~PID();

  /**
   * Initialize PID.
   * @param (Kp_, Ki_, Kd_) The initial PID coefficients
   */
  void Init(double Kp_, double Ki_, double Kd_);

  /**
   * Update the PID error variables given cross track error.
   * @param cte The current cross track error
   */
  void UpdateError(double cte);

  /**
   * Calculate the total PID error.
   * @output The total PID error
   */
  double TotalError();

  /**
   * Parameter optmization method
   * @param p Base parameter value
   * @param dp Probing value
  */

  void Twiddle(double error);

  void ParameterTuner(int index, double value);



 private:
  /**
   * PID Errors
   */
  double p_error;
  double i_error;
  double d_error;

  /**
   * PID Coefficients
   */
  double Kp;
  double Ki;
  double Kd;

  // Previous cte
  double prev_cte;

  // Parameter tuning variables
  double best_error;
  double total_error;
  int evaluation_steps;
  int counter;
  int p_index;
  bool increase;
  bool decrease;
  std::array<double, 3> p;

};

#endif  // PID_H
