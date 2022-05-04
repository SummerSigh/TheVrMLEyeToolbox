![GitHub Logo](/images/logo.png)
A repo containing several methods for near-eye gaze tracking in HMDs.

**This repo is a work in progress**

*What is this all about?*

- this repo is for the EyetrackVR project aiming to make VR eyetracking open-source and available to everyone. More specifically, this repo focuses on ML or DL based approaches for eye tracking.

*What can I do to help?* 

- You can DM me at Summer#2406 on Discord if you have any ideas, or want to submit data from your eye tracker!

*Where is the Hardware?*

- You can look at https://github.com/RedHawk989/EyeTrackVR

Hardware will hopefully be a ESP32-CAM with a 160° FOV IR camera this is not confirmed and very likely could change. In terms of VRC implementaion, please look at the repo above. 

## ABOUT IR EMMITTER SAFETY
Please exercise extreme caution when messing around with IR emmitters.
Once safety testing has been completed, links and files will be provided for the emmitters. Please do not try to make or use any emmitters unless you know exactly what you are doing, as it could be very harmful for your eyes if not done correctly. 
When files and resources are released DO NOT BYPASS ANY SAFETY FEATURES PUT IN PLACE. This can result in a very harmful outcome. 
The saftey measures were put in place to REDUCE the potential falure risk. All further safety responsibilities are on the user.
This includes visually checking with an IR camera that the brightness is correct.

**Make sure you are using NON-focused emitters and at around 5 mA total power**

https://www.ncbi.nlm.nih.gov/labs/pmc/articles/PMC3116568/

https://www.osha.gov/sites/default/files/training-library_nir_stds_20021011.ppt

https://dammedia.osram.info/media/bin/osram-dam-2496608/AN002_Details%20on%20photobiological%20safety%20of%20LED%20light%20sources.pdf

## Firmware
Current testing has been performed with loucass003's firmware found here https://github.com/Futurabeast/futura-face-cam
There has been work on a different firmware by a community member, but that has not been tested by me here https://github.com/lorow/OpenIris

Implemented methods:
- [X] YoloV5 Iris Detection (ML model is subject to updates)
- [X] Pupil Locator CNN Model  
- [X] RANSAC Contours <----- Currently the best eye tracking system in this repo
- [X] 2D to 3D Point Infrence (calibration based 3d model fitting)
- [ ] EMG Facial Interface for Eye Muscle Traking (Hardware will be provided here) 

**NOTE: Some of these implemented methods will be from other authors and maybe subject to licensing.**






***Citations for the people who make this all possible***

@inproceedings{chaudhary2019ritnet,
  title={RITnet: real-time semantic segmentation of the eye for gaze tracking},
  author={Chaudhary, Aayush K and Kothari, Rakshit and Acharya, Manoj and Dangi, Shusil and Nair, Nitinraj and Bailey, Reynold and Kanan, Christopher and Diaz, Gabriel and Pelz, Jeff B},
  booktitle={2019 IEEE/CVF International Conference on Computer Vision Workshop (ICCVW)},
  pages={3698--3702},
  year={2019},
  organization={IEEE}
}

@article{yiu2019deepvog,
  title={DeepVOG: Open-source Pupil Segmentation and Gaze Estimation in Neuroscience using Deep Learning},
  author={Yiu, Yuk-Hoi and Aboulatta, Moustafa and Raiser, Theresa and Ophey, Leoni and Flanagin, Virginia L and zu Eulenburg, Peter and Ahmadi, Seyed-Ahmad},
  journal={Journal of neuroscience methods},
  year={2019},
  publisher={Elsevier}
}

Shaharam Eivazi, Thiago Santini, Alireza Keshavarzi, Thomas Kübler, and Andrea Mazzei. 2019.
Improving real-time CNN-based pupil detection through domain-specific data augmentation.
In Proceedings of the 11th ACM Symposium on Eye Tracking Research & Applications (ETRA ’19).
Association for Computing Machinery, New York, NY, USA, Article 40, 1–6.
DOI:https://doi.org/10.1145/3314111.3319914



