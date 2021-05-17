# Data_hw3

##資料處理和判讀

資料主要由時間(time)、生產(generation)、消耗(consumption)構成。

時間共有數月的資料，有每一個小時當下的生產電量和消耗電量

下圖圖示為生產電量的

![image1](https://i.imgur.com/VFVWMNd.png)

可以看出具有週期性(Seansonal)，週期為一天，也就是24個單位

下圖圖示為消耗電量

![image2](https://i.imgur.com/7Rsgb8e.png)

雖然左右兩個相對突出，不過依然具有相似的走勢，週期一樣為24個單位

## 模型分析:

使用Seasonal Arima，先使用Auto Arima來調整參數，最後(p,d,q)選擇(2,1,0)，而Seasonal的參數(P,D,Q,S)為(1,1,1,24)，最後一個參數24代表週期

下圖為預測出來產生電量的圖示

![image3](https://i.imgur.com/4gEALPJ.png)

讀取的資料為前七日，左側藍色為七日資料中最後一日(24筆)的產電量，右邊紅色為預測第八日的產電量，可以看出趨勢相當

下圖則為預測出來消耗電量的圖示

![image4](https://i.imgur.com/rrrw8na.png)

左側藍色為七日資料中最後一日的用電量，右邊紅色為預測第八日的用電量

基本上趨勢能預測出來，如用電高峰發電高峰能明確地抓出。
