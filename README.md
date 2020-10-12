# PID Controller
Control the steering and throttle using PID algorithm

## Objective
1. Write a PID controller in C++ that can drive the car around the track in the Udacity's simulator
2. Tune the hyperparameters so that the car drives smoothly around the track
3. Implement a parameter optmization algorithm that can tune the parameters continuously
4. Increase the speed of the car upto 100 mph or its breaking point

### Algorithm Overview:
PID controller is a basic type of controller used to achieve a steady state of a system. This works as a feedback loop with the system returning a Cross Track Error (CTE) and the PID algorithm working towards minimizing that error.

The equation for PID is given by:

&alpha; = -&tau;</sub>p _CTE_  - &tau;</sub>i _CTE_ - &tau;</sub>d _CTE_

Where:
 - &tau;</sub>p is the Proportional component of the &alpha;
 - &tau;</sub>i is the Integral component of the &alpha;
 - &tau;</sub>d is the Derivative component of the &alpha;  
 - &alpha; is the total error that is passed back to the system


Proportional component of the &alpha; is responsible towards returning a value that directory reduces
the CTE for that moment in time. While this is great in bringing down the CTE instantly, it also causes overshoot and results in an oscillation.   

To counteract these oscillations, Derivative part of the &alpha; works as a resistance to the Proportional component and pulls the system away from sudden change in the CTE value. This helps reduce the oscillation in the system.

Integral part of the &alpha; only comes into play when the system reaches a steady state error. One of the reason this might occur is if the system has a constant bias which pulls the system away from converging. In this scenario, the accumulated error from the integral part will help the system converge.

### Parameter Optmization

As a first step, I went on to manually tune the parameters to get a best state estimate of a stable system. At first, I set all the other parameters to zero. Then,
- I started to increase the Proportional part of PID controller from `0` up until the car in the simulator started oscillating. I chose a value of `0.085` for steering control and `0.2` for throttle control.

- Once I found a starting value for Proportional controller, I increased Derivative part up until the car stopped oscillating. This was around `3.0` for steering control and `0.045` for throttle control.

- The Integral controller is largely unused since the simulator did not have any systemic bias. Therefore I chose a small value of `0.0001` for have minimal influence on this system.

After settling on a base set of values from the above approach, it was time to implement an algorithm that would continuously tune the parameters based on CTE for that time. Introducing **Twiddle**.

Twiddle algorithm tunes each of the hyperparameters to minimize the CTE. I have set the test loop in PID.cpp for 200 cycles, meaning, each tuned parameter runs for 200 cycles and then Twiddle checks if the tuned parameter is good enough. If it is good, it keeps the value, otherwise, it increases or decreases the value by a small probing amount and tests again.

### Result

My code runs on two modes. One with a constant acceleration of 0.35 which keeps the vehicle at about 35 mph and the other with an initial throttle value of 0.85 which achieves the speeds up to 85 mph. Toggle the `fast_mode` in `main.cpp` to switch either one or the other.

![clip_optmized](https://user-images.githubusercontent.com/8539470/95699192-d0ae6700-0c11-11eb-9a05-474314bed6bf.gif)

### Future Work

In the fast mode the car picks up velocity in the straightaway (especially when the CTE is close to zero) and doesn't account for the upcoming sharp turn. This causes the car to react too late for the turn and bumps over the curb. An insight of the map of the track would be really helpful in modeling the throttle parameter.

## Dependencies

* cmake >= 3.5
 * All OSes: [click here for installation instructions](https://cmake.org/install/)
* make >= 4.1(mac, linux), 3.81(Windows)
  * Linux: make is installed by default on most Linux distros
  * Mac: [install Xcode command line tools to get make](https://developer.apple.com/xcode/features/)
  * Windows: [Click here for installation instructions](http://gnuwin32.sourceforge.net/packages/make.htm)
* gcc/g++ >= 5.4
  * Linux: gcc / g++ is installed by default on most Linux distros
  * Mac: same deal as make - [install Xcode command line tools]((https://developer.apple.com/xcode/features/)
  * Windows: recommend using [MinGW](http://www.mingw.org/)
* [uWebSockets](https://github.com/uWebSockets/uWebSockets)
  * Run either `./install-mac.sh` or `./install-ubuntu.sh`.
  * If you install from source, checkout to commit `e94b6e1`, i.e.
    ```
    git clone https://github.com/uWebSockets/uWebSockets
    cd uWebSockets
    git checkout e94b6e1
    ```
    Some function signatures have changed in v0.14.x. See [this PR](https://github.com/udacity/CarND-MPC-Project/pull/3) for more details.
* Simulator. You can download these from the [project intro page](https://github.com/udacity/self-driving-car-sim/releases) in the classroom.
