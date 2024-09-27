import streamlit as st
from vyzeai.agents.prebuilt_agents import ResearchAgent, LinkedInAgent, EmailAgent, VideoAudioBlogAgent, YTBlogAgent

if 'api_key' not in st.session_state:
    st.session_state['api_key'] = None
if 'content' not in st.session_state:
    st.session_state['content'] = None
if 'image_path' not in st.session_state:
    st.session_state['image_path'] = None
if 'file_path' not in st.session_state:
    st.session_state['file_path'] = None

# st.write(st.session_state)
st.title("LinkedIn Manager")

api_key = st.text_input("Enter opeani api key", type='password', key='api_key')
option = st.selectbox("Select soruce", ('website', 'youtube', 'video/audio'), placeholder="choose one", key='selectbox_option')
if option == 'website':
    topic = st.text_input("Enter the topic", key='topic')
    url = st.text_input("Enter a website url", key='url')
if option == 'youtube':
    yt_url = st.text_input("Enter a YouTube url", key='yt_url')
if option == 'video/audio':
    file = st.file_uploader("Upload video or audio file", type=['mp4', 'mp3'], key='video/audio')
    with open(file.name, "wb") as f:
        f.write(file.getbuffer())
    st.session_state['file_path'] = file.name

if st.session_state.api_key:
    if st.button("submit"):
        if st.session_state['selectbox_option'] == 'website':
            research_agent = ResearchAgent(st.session_state.api_key)
            linkedin_agent = LinkedInAgent(st.session_state.api_key)

            context = research_agent.research(topic, url)

            content, image_path = linkedin_agent.generate_linkedin_post(context)
            st.write(content)
            st.image(image_path)
            st.session_state['content'] = content
            st.session_state['image_path'] = image_path
            
        if st.session_state['selectbox_option'] == 'youtube':
            # research_agent = ResearchAgent(st.session_state.api_key)
            yt_agent = YTBlogAgent(api_key)
            linkedin_agent = LinkedInAgent(st.session_state.api_key)

            # context = research_agent.research(topic, url)
            context = yt_agent.extract_transcript(st.session_state.yt_url)

            content, image_path = linkedin_agent.generate_linkedin_post(context)
            st.write(content)
            st.image(image_path)
            st.session_state['content'] = content
            st.session_state['image_path'] = image_path

        if st.session_state['selectbox_option'] == 'video/audio':
            # research_agent = ResearchAgent(st.session_state.api_key)
            va_agent = VideoAudioBlogAgent(api_key)
            linkedin_agent = LinkedInAgent(st.session_state.api_key)

            # context = research_agent.research(topic, url)
            context = va_agent.extract_text(st.session_state.file_path)

            content, image_path = linkedin_agent.generate_linkedin_post(context)
            st.write(content)
            st.image(image_path)
            st.session_state['content'] = content
            st.session_state['image_path'] = image_path

    if st.session_state.content:
        token = st.text_input("Enter LinkedIn Oauth token", key='token')
        
        if st.button("post on linkedin", key='linkedin_post_button'):
            linkedin_agent = LinkedInAgent(api_key)
            ack = linkedin_agent.post_content_on_linkedin(token, st.session_state.content, st.session_state.image_path)
            st.write(ack)

                



