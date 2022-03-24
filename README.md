![GitHub Logo](/images/logo.png)
A repo containing several methods for near eye gaze tracking in HMDs

**This Repo is a work in progress**

*What is this all about?*

- this repo is for the EyetrackVR project aiming to make VR eyetracking opensource and available to everyone. More specifically, this repo focuses on ML or DL based approaches for eye tracking.

*What can I do to help?* 

- You can DM me at Summer#2406 on Discord if you have any ideas, or want to submit data from your eye tracker!

*Where is the Hardware?*

- You can look at https://github.com/RedHawk989/EyeTrackVR


Implemented methods:
- [X] YoloV5 iris detection (ML model is subject to updates)
- [X] Pupil Locator CNN Model <----- current best 
- [ ] 2d to 3d point infrence using calibration based 3d model fitting
- [ ] Glint tracking
- [ ] EMG Facial interface for Eye muscle tracking (Hardwear will be provided here) 
- [ ] Landmark Based tracking

**NOTE: Some of these implemented methods will be from other authors and maybe subject to licencing.**






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



