#include "PID.h"
#include <limits>
#include <iostream>

/**
 * TODO: Complete the PID class. You may add any additional desired functions.
 */

PID::PID() {}

PID::~PID() {}

void PID::Init(double Kp_, double Ki_, double Kd_) {
  /**
   * TODO: Initialize PID coefficients (and errors, if needed)
   */
   Kp = Kp_;
   Ki = Ki_;
   Kd = Kd_;

   // Initialize errors
   p_error = 0;
   d_error = 0;
   i_error = 0;

   // Initialize previous CET to zero
   prev_cte = 0;

   // Initialize best error to max Value
   best_error = std::numeric_limits<double>::max();
   total_error = 0;

   // Parameter tuning variables
   evaluation_steps = 100;
   counter = 1;
   p_index = 0;
   increase = false;
   decrease = false;

   p.at(0) = 0.2 * Kp;
   p.at(1) = 0.2 * Ki;
   p.at(2) = 0.2 * Kd;

}

void PID::UpdateError(double cte) {
  /**
   * TODO: Update PID errors based on cte.
   */

   p_error = cte;
   d_error = cte - prev_cte;
   i_error += cte;
   prev_cte = cte;


   /**
      Parameter optmization using Twiddle algorithm
   **/
   total_error += cte * cte;

   if(counter % evaluation_steps == 0)
   {
     Twiddle(total_error);
   }

   ++counter;

}

double PID::TotalError() {
  /**
   * TODO: Calculate and return the total error
   */

   return -Kp*p_error - Kd*d_error - Ki*i_error;
}

void PID::Twiddle(double error)
{
  // If the error is better than best estimate we have, keep the new error
  if(error < best_error)
  {
    best_error = error;
    p[p_index] *= 1.1;

    // Tune the parameters
    increase = false;
    decrease = false;
  }

  // Tune the parameters
  if(!increase && !decrease)
  {
    // First iteration - try increasing the parameter value
    ParameterTuner(p_index, p[p_index]);
    increase = true;
  }
  else if(increase && !decrease)
  {
    // Second iteration - try decreasing the parameter value
    ParameterTuner(p_index, -2*p[p_index]);
    decrease = true;
  }
  else
  {
    // If no best error found, keep the previous best known error
    ParameterTuner(p_index, p[p_index]);
    p[p_index] *= 0.9;
    increase = false;
    decrease = false;

    // Tune the next parameter
    p_index = (p_index+1) % 3;
  }

  // Print twiddle parameters
  std::cout << "------Twiddle parameters:------ \n" ;
  std::cout << "Kp: " << Kp << " Ki: " << Ki << " Kd: " << Kd << "\n\n";
}

void PID::ParameterTuner(int index, double value)
{
  switch(index)
  {
    case 0:
      Kp += value;
      break;

    case 1:
      Ki += value;
      break;

    case 2:
      Kd += value;
      break;

    default:
      break;
  }

}
