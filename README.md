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

**Make sure you are using NON-focused emitters and at around 5 mA total power**

Try visually checking with an IR camera to see if the the brightness is correct. **If you feel any sensation around your while wearing a DIY eye tracker, DO NOT ATTEMPT TO USE THE TRACKER UNTIL YOU HAVE LOWERED THE AMOUNT OF LIGHT COMING FROM THE EMMITERS.** Continue process until no heat, tingling, or the sesnation of a bright light is present. 

https://www.ncbi.nlm.nih.gov/labs/pmc/articles/PMC3116568/

https://www.osha.gov/sites/default/files/training-library_nir_stds_20021011.ppt

https://dammedia.osram.info/media/bin/osram-dam-2496608/AN002_Details%20on%20photobiological%20safety%20of%20LED%20light%20sources.pdf

**(This research was provided by Prohurtz in their repo: https://github.com/RedHawk989/EyeTrackVR)**

## Firmware

Current testing has been performed with loucass003's firmware found here https://github.com/Futurabeast/futura-face-cam
There has been work on a different firmware by a community member, but that has not been tested by me here https://github.com/lorow/OpenIris


Implemented methods:
- [X] YoloV5 Iris Detection (Deprecated)
- [X] Pupil Locator CNN Model (Updates Soon) 
- [X] RANSAC Eye <----- Currently the best eye tracking 2d system in this repo (subject to QOL and Enchancements) 
- [X] 2D to 3D Point Infrence (calibration based 3d model fitting. Not a tracking method)
- [ ] EMG Facial Interface for Eye Muscle Tracking (Hardware will be provided here) 


**NOTE: Some of these implemented methods will be from other authors and may be subject to licensing.**
===
## Quick start guide

For a quick start guide in VRC please refer to **Pupil3dDectectorOSC** folder

If you want to use the raw aglorithm with 3d pupil fiting for your own purposes look at the **Pupil3dDectector** folder

If you want to use just the raw 2d algorithm for your own purposes please refer to the **RANSAC Eye** folder 

**NOTE: Some of these implemented methods will be from other authors and maybe subject to licencing.**






## Citations for the people who make this all possible

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



