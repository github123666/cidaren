#
str_ = "XLk9Si4e2Mli0AtCepWIx97pBB8EtrFveyJ0YXNrX2lkIjo5MTE1ODUxMCwidGFza190eXBlIjozLCJ0b3BpY19tb2RlIjozMiwic3RlbSI6eyJjb250ZW50IjoiXyAgXyIsInJlbWFyayI6Iue8k+ino+e0p+W8oCIsInBoX3VzX3VybCI6bnVsbCwicGhfZW5fdXJsIjpudWxsLCJhdV9hZGRyIjpudWxsfSwib3B0aW9ucyI6W3siY29udGVudCI6InJlbGlldmUiLCJyZW1hcmsiOm51bGwsImFuc3dlciI6bnVsbCwiYW5zd2VyX3RhZyI6MCwiY2hlY2tfY29kZSI6bnVsbCwic3ViX29wdGlvbnMiOm51bGwsInBoX2luZm8iOm51bGx9LHsiY29udGVudCI6InRlbnNpb24iLCJyZW1hcmsiOm51bGwsImFuc3dlciI6bnVsbCwiYW5zd2VyX3RhZyI6MSwiY2hlY2tfY29kZSI6bnVsbCwic3ViX29wdGlvbnMiOm51bGwsInBoX2luZm8iOm51bGx9LHsiY29udGVudCI6ImNvbnNlcnZhdGlvbiIsInJlbWFyayI6bnVsbCwiYW5zd2VyIjpudWxsLCJhbnN3ZXJfdGFnIjoyLCJjaGVja19jb2RlIjpudWxsLCJzdWJfb3B0aW9ucyI6bnVsbCwicGhfaW5mbyI6bnVsbH0seyJjb250ZW50Ijoic3VyZmFjZSIsInJlbWFyayI6bnVsbCwiYW5zd2VyIjpudWxsLCJhbnN3ZXJfdGFnIjozLCJjaGVja19jb2RlIjpudWxsLCJzdWJfb3B0aW9ucyI6bnVsbCwicGhfaW5mbyI6bnVsbH1dLCJzb3VuZF9tYXJrIjoiIiwicGhfZW4iOiIiLCJwaF91cyI6IiIsImFuc3dlcl9udW0iOjEsImNoYW5jZV9udW0iOjEsInRvcGljX2RvbmVfbnVtIjo0MCwidG9waWNfdG90YWwiOjQ5LCJ3X2xlbnMiOltdLCJ3X2xlbiI6MCwid190aXAiOiIiLCJ0aXBzIjoi5o6S5YiX5ZCI6YCC55qE5Y2V6K+N57uE5oiQ55+t6K+tIiwid29yZF90eXBlIjoxLCJlbmFibGVfaSI6MiwiZW5hYmxlX2lfaSI6MiwiZW5hYmxlX2lfbyI6MiwidG9waWNfY29kZSI6ImtsZDRlNHBzbDlMVG1WS1JWM2w4akd5WW9xckhsMmRuV21KYnFwclQxNStqejRWbFoybU9hR1pzYm1ka2s0VFRtWnpPbXF5Y1pLeWVvS3ZMcDZWWWxXS1VXS2ZLMEorWjE4aFpxSnpRcXA2a3BGaVZaSk9OWlZ5V2JHWnBjVzlzWW5DU2JHeHJaSkdXWW1tVmtHcHRqWnB1YVcyWWIyMWhhV0p4YVpPV2JHV1daV0pvYTNGdGEycWFibTVpYUdKcGt3PT0iLCJhbnN3ZXJfc3RhdGUiOjF9"
str_2 = "SIZSflxwwyIrYqknOjWpOLb9i7EPulFzeyJ3b3JkIjoidG91Z2giLCJ0b3BpY19jb2RlIjoia2xkNGU0cHNsOUxUbVZLUlYzbDhqR3lZb3FySGwyZG5XbUpicXFUYXk1NVdqWlJxWUdxWWJtR1FhWk5razcrTlpWeVdZV2R1YUdwd2EyMllhbXB1Y1dabGtaQ1Z3V0tQbE1DV1lHaVNZMmx1WW0xdGJaaVhiR2lSYUdKd2FXbHVhbTJUYUdObmEyOXRiMmVkbW0xZ2tZOXBrUT09Iiwib3Zlcl9zdGF0dXMiOjEsImFuc3dlcl9yZXN1bHQiOjEsImNsZWFuX3N0YXR1cyI6MiwiYW5zd2VyX2NvcnJlY3RzIjpbM119"
import base64

data = base64.b64decode(str_).decode("utf-8", errors='ignore')
print(data)
# import brotli
# brotli.decompress()