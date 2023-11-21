# 间隔时间(秒)
intervalTime=1800

while true
do
	echo "Running Python script..."
	python3 main_bili.py

	echo "BiliBili download Waiting for a few minute..."
	while true
	do
		current_time=$(date +"%Y:%m:%d %H:%M:%S")
		echo "sleep $intervalTime bilibili  Current Time: $current_time"
		sleep $intervalTime
		python3 main_bili.py
	done
done

