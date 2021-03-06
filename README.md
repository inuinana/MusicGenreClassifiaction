# Content-based Music Genre Classification


## Complete Installation

1. Install sox and/or ffmpeg (see below)
2. Clone this project
3. Go to the folder(MusicGenreClassification)
4. bash run_me_first.sh (This process takes for a while as it downloads the entire dataset)
* You may need to install sox and/or ffmpeg if you do not have one. (Windows complains sometimes..) 

For installing sox (Windows)
https://sourceforge.net/projects/sox/

For installing sox (Mac)
http://macappstore.org/sox/

For installing ffmpeg
https://www.ffmpeg.org/download.html
or 
brew install ffmpeg

* Make sure you are using Python3


## About

The automatic classification system to the most widely used music dataset; the GTZAN Music Genre Dataset was implemented. 
The system was implemented with a set of low-level features, mel-spectorogram and several supervised classification methods.


## Dataset
The GTZAN Music Genre Dataset, which is a collection of 1000 songs in 10 genres, is the most widely used dataset. 

Although many studies have been conducted using GTZAN, several faults have been pointed out. Sturm[1], for example, identified and analysed the contents of GTZAN and provided a catalogue of its faults. As it is the most used dataset, however, the system performance of MGC in this project should first be evaluated with GTZAN in order to compare against other systems used in other studies.

Details on the GTZAN Music Genre Dataset are presented in the table below. In GTZAN, each song is recorded at a sampling rate of 22.05 kHz and mono 16-bit audio files in .wav format.

<p align="center">
<img src="assets/GTZAN.png?raw=true" alt="GTZAN" width="500">
</p>

## Pre-processing
All songs are converted to 44.1kHz, 32bit, .wav format with 10 seconds.  
(see backend/src/data_process/audio_dataset_maker.py)

The input audio signal is segmented into analysis windows of 46ms (customizable) length with an overlap of half size of an analysis window. The number of samples in an analysis window is usually the equal power of two to facilitate the use of FFT. For the system, 2048 samples are framed for an analysis window. Also, hamm widow is applied to each analysis window.

## Feature Extraction

In this project, 2 types of audio features are extracted.  
1. Hand crafted low-level audio feature 2. Mel-spectrogram

### 1. Hand crafted low-level audio feature (Expert system)
<p align="center">
<img src="assets/Ex.png?raw=true" alt="Feature Extraction" width="600">
</p>

Ten types of low-level feature—six short-term and four long-term features—noted are extracted from the analysis windows and texture windows, respectively. In order to characterise the temporal evaluation of the audio signal, long-term features are computed by aggregating the short-term features.

<p align="center">
<img src="assets/Features.png?raw=true" alt="Feature Extraction" width="300">
</p>

Over a texture window which consists of 64 analysis windows, short-term features are integrated with mean values.

### 2. Mel-spectrogram
Also, mel-spectrogram is extracted from the entire audio.

<p align="center">
<img src="assets/mel_spectrogram.png?raw=true" alt="Feature Extraction" width="800">
</p>

## Classifier
k-NN

This method uses Euclidean distance between training and testing data. Each test sample is classified depending on the k number of training samples that surround the test sample. 


Multilayer Perceptron

The multilayer Perceptron to this project consists of 3 layers with relu function. The training data is splitted into 10% for the validation and 90% for the training. It loads the data from "Data.csv".

Logistic Regression


Convolutional Neural Network



## Results
k-NN: 62.0%
MLP: 83.6%
Logistic Regression: 70.3%

### Dependency
Please see requirements.txt

## References
[1] B. L.Sturm, "The GTZAN dataset: Its contents, its faults, their effects on evaluation, and its
future use," arXiv preprint arXiv:1306.1461, 2013.

[2] E.Loweimi, S. M. Ahadi, T. Drugman and S. Loveymi, "On the importance of pre-emphasis
and window shape in phase-based speech recognition," in International Conference on
Nonlinear Speech Processing(pp. 160-167). Springer, Berlin, Heidelberg, June, 2013.

[3] K. K. Chang, J. S. R. Jang and C. S. Iliopoulos, "Music Genre Classification via Compressive
Sampling," in ISMIR, pp. 387-392, August, 2010.

[4] B. L. Sturm, "On music genre classification via compressive sampling," in Multimedia and
Expo (ICME), 2013 IEEE International Conference on (pp. 1-6). IEEE, July, 2013.

[5] Keller, M. R. Gray and J. A. Givens, A fuzzy k-nearest neighbor algorithm. IEEE
transactions on systems, man, and cybernetics, (4), pp.580-585, 1985.

[6] http://benanne.github.io/2014/08/05/spotify-cnns.html

## Author

Akihiro Inui
http://www.portfolio.akihiroinui.com


## License

MusicGenreClassification is available under the MIT license. See the LICENSE file for more info.

