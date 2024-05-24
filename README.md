## Generate .srt subtitles from a video file using OpenAI Whisper.  
CLI mode:  
> python main.py path/to/your/video.mp4 --cli --sync --keep-intermediate --video-lang eng --sub-lang eng --output-path /path/to/output

--cli runs without GUI.  
--sync runs subsync after gemeration.  
--keep-intermediate Refrains from deleting temporary files like extracted audio.  
--video-lang and --sub-lang are optional parameters for subsync  

GUI mode is pretty self explanatory.
