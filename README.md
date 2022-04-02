"# Major-Project" 

To intialize the code 


1)Start with visual studio code, Download visual studio code according to your laptop configuration 

2)Install mini conda PYTHON 3.8-3.10 version windows or mac depending on the laptop used.

3)Now START VS CODE AND write 
--conda install git 
-Now after installing the git create a new environment 
--conda create -n gati
--conda activate gati
--git clone https://github.com/DhruvTh/Major-Project.git
--cd Major-Project

4)Follow the steps given in - https://towardsdatascience.com/realtime-multiple-person-2d-pose-estimation-using-tensorflow2-x-93e4c156d45f
-(In the above process do not need to clone "git clone https://github.com/gsethi2409/tf-pose-estimation.git" and Download the built-in tools from https://visualstudio.microsoft.com/visual-cpp-build-tools/ and install it to avoid error while installing the packages (Do not need to do it for mac and linux))

5)After that run the following commands to install required packages,
--pip install pandas
--pip install flask
--pip install pyserial
--pip install openpyxl


(To run the GPU, instead of pip install tensorflow do the "conda install -c anaconda tensorflow-gpu" which installs the GPU version. For this make sure to work on python compatible environment such as python 3.8-3.10)
