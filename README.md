# cross_domain_baseline
## 配置环境
```
conda env create -f environment.yml
```
## AS-MAML的运行方法
1、把Log-Fusion预处理的数据集放到data目录下  
2、然后修改mytest.py中的preprocess(参数)，运行mytest.py获取符合AS-MAML输入格式的数据集  
3、其次，修改data目录下的dataset1.py文件，在第46行按照前面的格式补充当前数据集的特征数量，同时修改第52行代码，加上该数据集的名称   
4、最后，修改main.py中的数据集，运行main.py  
  
## GraphFewShot的运行方法
1、数据集放到datasets目录下  
2、修改prepare_checkpoints.sh，仿照之前的格式添加新的数据集，然后powershell运行prepare_checkpoints.sh  
3、修改datasets目录下的main_preprocess.py中的dataset_name，运行main_preprocess.py  
4、修改main.py数据集名，运行即可  

## Meta-MGNN的运行方法
1、数据集放到Original_datasets目录下  
2、修改samples.py的第15行代码，仿照之前的格式添加新数据集相关信息  
3、修改main.py的数据集名称，运行main.py  


