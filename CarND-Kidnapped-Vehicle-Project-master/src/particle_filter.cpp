/**
 * particle_filter.cpp
 *
 * Created on: Dec 12, 2016
 * Author: Tiffany Huang
 */

#include "particle_filter.h"

#include <math.h>
#include <algorithm>
#include <iostream>
#include <iterator>
#include <numeric>
#include <random>
#include <string>
#include <vector>
#include <cassert>

#include "helper_functions.h"

using std::string;
using std::vector;

void ParticleFilter::init(double x, double y, double theta, double std[]) {
  /**
   * TODO: Set the number of particles. Initialize all particles to
   *   first position (based on estimates of x, y, theta and their uncertainties
   *   from GPS) and all weights to 1.
   * TODO: Add random Gaussian noise to each particle.
   * NOTE: Consult particle_filter.h for more information about this method
   *   (and others in this file).
   */
  num_particles = 50;  // TODO: Set the number of particles

  std::default_random_engine gen;
  std::normal_distribution<double> dist_x(x,std[0]);
  std::normal_distribution<double> dist_y(y,std[1]);
  std::normal_distribution<double> dist_theta(theta,std[2]);
  weights.resize(num_particles);
  particles.resize(num_particles);
  for(int i=0; i < num_particles; ++i)
  {
    particles.at(i).id = i;
    particles.at(i).x = dist_x(gen);
    particles.at(i).y = dist_y(gen);
    particles.at(i).theta = dist_theta(gen);
    particles.at(i).weight = 1;
    weights.at(i) = 1;
  }

  // set initialization status
  is_initialized = true;
}

void ParticleFilter::prediction(double delta_t, double std_pos[],
                                double velocity, double yaw_rate) {
  /**
   * TODO: Add measurements to each particle and add random Gaussian noise.
   * NOTE: When adding noise you may find std::normal_distribution
   *   and std::default_random_engine useful.
   *  http://en.cppreference.com/w/cpp/numeric/random/normal_distribution
   *  http://www.cplusplus.com/reference/random/default_random_engine/
   */
    
    // generate random noise
    std::default_random_engine gen;
    std::normal_distribution<double> dist_x(0,std_pos[0]);
    std::normal_distribution<double> dist_y(0,std_pos[1]);
    std::normal_distribution<double> dist_theta(0,std_pos[2]);

   for(auto& particle : particles)
   {
     // if the vehicle is not moving in the straight line
     if(fabs(yaw_rate) > 0.000001)
     {
       double normalizer = velocity/yaw_rate;
       particle.x += normalizer*(std::sin(particle.theta + (yaw_rate*delta_t))
                                  - std::sin(particle.theta));
       particle.y += normalizer*(std::cos(particle.theta)
                                  - std::cos(particle.theta + (yaw_rate*delta_t)));

       particle.theta += (yaw_rate*delta_t);
     }

     // if the vehicle is moving in straight line
     else
     {
       particle.x += velocity*delta_t*std::cos(particle.theta);
       particle.y += velocity*delta_t*std::sin(particle.theta);

       // generate random noise
       std::default_random_engine gen;
       std::normal_distribution<double> dist_x(particle.x,std_pos[0]);
       std::normal_distribution<double> dist_y(particle.y,std_pos[1]);
       std::normal_distribution<double> dist_theta(particle.theta,std_pos[2]);
     }
       
       // add noise to particle pose
       particle.x += dist_x(gen);
       particle.y += dist_y(gen);
       particle.theta += dist_theta(gen);
   }

}

void ParticleFilter::dataAssociation(vector<LandmarkObs> predicted,
                                     vector<LandmarkObs>& observations) {
  /**
   * TODO: Find the predicted measurement that is closest to each
   *   observed measurement and assign the observed measurement to this
   *   particular landmark.
   * NOTE: this method will NOT be called by the grading code. But you will
   *   probably find it useful to implement this method and use it as a helper
   *   during the updateWeights phase.
   */

}

void ParticleFilter::updateWeights(double sensor_range, double std_landmark[],
                                   const vector<LandmarkObs> &observations,
                                   const Map &map_landmarks) {
  /**
   * TODO: Update the weights of each particle using a mult-variate Gaussian
   *   distribution. You can read more about this distribution here:
   *   https://en.wikipedia.org/wiki/Multivariate_normal_distribution
   * NOTE: The observations are given in the VEHICLE'S coordinate system.
   *   Your particles are located according to the MAP'S coordinate system.
   *   You will need to transform between the two systems. Keep in mind that
   *   this transformation requires both rotation AND translation (but no scaling).
   *   The following is a good resource for the theory:
   *   https://www.willamette.edu/~gorr/classes/GeneralGraphics/Transforms/transforms2d.htm
   *   and the following is a good resource for the actual equation to implement
   *   (look at equation 3.33) http://planning.cs.uiuc.edu/node99.html
   */

   int iParticle = 0;
   for(auto& particle : particles)
   {
     // perform data association
     vector<LandmarkObs> temp_observations = observations;
     vector<LandmarkObs> associated_landmark(observations.size());
     particle.weight = 1;
     int iObservation = 0;
     for(auto& observation : temp_observations)
     {
       // convert each observation from vehicle coordinate system to global space
       observation.x = particle.x + (std::cos(particle.theta)*observation.x)
                                       - (std::sin(particle.theta)*observation.y);
       observation.y = particle.y + (std::sin(particle.theta)*observation.x)
                                       + (std::cos(particle.theta)*observation.y);


       // initialize observation id
       observation.id = -1;
       double shortest_distance = std::numeric_limits<double>::infinity();
       for(auto& landmark : map_landmarks.landmark_list)
       {
         double distance = dist(landmark.x_f, landmark.y_f, observation.x, observation.y);
         double distance_to_landmark = dist(particle.x, particle.y, landmark.x_f, landmark.y_f);

         // assign the landmark id of shortest_distance to observation
         if(distance < shortest_distance && distance_to_landmark < sensor_range)
         {
           shortest_distance = distance;
           observation.id = landmark.id_i;

           // store this landmark as an associated landmark
           associated_landmark.at(iObservation).id = landmark.id_i;
           associated_landmark.at(iObservation).x = landmark.x_f;
           associated_landmark.at(iObservation).y = landmark.y_f;
           //std::cout << "Distance to particle "<< iParticle << " is: "<<distance;
         }
         //std::cout << " Shortest distance for observation: "<< iObservation<< " is: " << shortest_distance <<std::endl;
       }

       // throw an error if the observation id is not updated
       assert(observation.id != -1);

       // update the weight of the particle with the landmark and observation
         assert(observation.id == associated_landmark.at(iObservation).id);
        particle.weight *= multiv_prob(std_landmark[0], std_landmark[1],
                                   observation.x, observation.y,
                                   associated_landmark.at(iObservation).x,
                                   associated_landmark.at(iObservation).y);

        ++iObservation;
     }

     //Update the weights vector
     weights.at(iParticle) = particle.weight;
     std::cout << "Weight for particle "<< iParticle << " is: "<< particle.weight << std::endl;

     // store the associated-landmark in vectors and set the association for each particle
     vector<int> associations(observations.size());
     vector<double> sense_x(observations.size());
     vector<double> sense_y(observations.size());
       int i = 0;
     for(auto landmark : associated_landmark)
     {
       associations.at(i) = landmark.id;
       sense_x.at(i) = landmark.x;
       sense_y.at(i) = landmark.y;
         i++;
     }
     SetAssociations(particle, associations, sense_x, sense_y);

     // increment iParticle
     ++iParticle;
   }
}

void ParticleFilter::resample() {
  /**
   * TODO: Resample particles with replacement with probability proportional
   *   to their weight.
   * NOTE: You may find std::discrete_distribution helpful here.
   *   http://en.cppreference.com/w/cpp/numeric/random/discrete_distribution
   */

   std::default_random_engine gen;
   std::discrete_distribution<long> dist_weights(weights.begin(), weights.end());
   std::vector<Particle> resampled_particles(particles.size());
   for(auto iParticle=0; iParticle<particles.size(); ++iParticle)
   {
       auto weight_chosen = dist_weights(gen);
       std::cout << "Chosen weight: " << weight_chosen << std::endl;
     resampled_particles.at(iParticle) = particles.at(weight_chosen);
   }
   particles = resampled_particles;

}

void ParticleFilter::SetAssociations(Particle& particle,
                                     const vector<int>& associations,
                                     const vector<double>& sense_x,
                                     const vector<double>& sense_y) {
  // particle: the particle to which assign each listed association,
  //   and association's (x,y) world coordinates mapping
  // associations: The landmark id that goes along with each listed association
  // sense_x: the associations x mapping already converted to world coordinates
  // sense_y: the associations y mapping already converted to world coordinates
  particle.associations= associations;
  particle.sense_x = sense_x;
  particle.sense_y = sense_y;
}

string ParticleFilter::getAssociations(Particle best) {
  vector<int> v = best.associations;
  std::stringstream ss;
  copy(v.begin(), v.end(), std::ostream_iterator<int>(ss, " "));
  string s = ss.str();
  s = s.substr(0, s.length()-1);  // get rid of the trailing space
  return s;
}

string ParticleFilter::getSenseCoord(Particle best, string coord) {
  vector<double> v;

  if (coord == "X") {
    v = best.sense_x;
  } else {
    v = best.sense_y;
  }

  std::stringstream ss;
  copy(v.begin(), v.end(), std::ostream_iterator<float>(ss, " "));
  string s = ss.str();
  s = s.substr(0, s.length()-1);  // get rid of the trailing space
  return s;
}

