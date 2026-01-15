def generate_script(topic):
    prompt = f"""
    Write a 1500-word monetizable YouTube script.
    Topic: {topic}

    Structure:
    - 15 sec hook
    - Curiosity gaps every 60 sec
    - Mid-roll friendly pacing
    - Neutral, factual tone
    - No greetings or CTA
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
def generate_metadata(topic):
    title = f"{topic} | What Nobody Tells You"
    description = (
        f"{topic} explained in depth.\n\n"
        "Watch till the end for key insights.\n\n"
        "#documentary #education"
    )
    tags = [
        topic,
        "explained",
        "documentary",
        "education",
        "deep dive"
    ]
    return title, description, tags
def create_thumbnail(text, output):
    img = Image.new("RGB", (1280, 720), "#121212")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arialbd.ttf", 85)

    headline = text.upper()[:28]
    draw.text((80, 280), headline, font=font, fill="#FFD700")

    img.save(output)
import subprocess
def create_short(long_video, output_short):
    command = [
        "ffmpeg",
        "-i", long_video,
        "-vf", "crop=ih*9/16:ih",
        "-t", "59",
        "-c:a", "aac",
        output_short
    ]
    subprocess.run(command, check=True)
def add_to_playlist(video_id, playlist_id, youtube):
    youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id }
            }
        }
    ).execute()
def schedule_time(index):
    return (datetime.utcnow() + timedelta(hours=4 * index)).isoformat() + "Z"
CHANNELS = [
    "client_secret_channel1.json",
    "client_secret_channel2.json"
]
