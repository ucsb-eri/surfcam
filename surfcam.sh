#!/bin/bash
ffmpeg -f lavfi -i anullsrc -rtsp_transport udp -i rtsp://<username>:<password>@<ip>:554//h264Preview_01_main -vf "[in]drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:textfile=/surf/data.txt:reload=1:fontcolor=white:fontsize=44:box=1:boxcolor=black@0.5:boxborderw=5:x=(w-text_w)/2:y=1300, drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:fontcolor=white:fontsize=44:box=1:boxcolor=black@0.8:text='%{localtime\:%m/%d/%y %T}':x=0:y=0[out]" -preset ultrafast -tune fastdecode -c:v libx264 -pix_fmt yuv420p -b:v 9500k -maxrate 9500k -bufsize 9500k -f flv -g 4 rtmp://a.rtmp.youtube.com/live2/<youtubekey>
