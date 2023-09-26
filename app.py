import pickle
import pandas as pd
import streamlit as st

st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)

st.markdown(
    """
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <a class="navbar-brand" href="#">YPL</a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav mr-auto">
           <li class="nav-item active">
            <a class="nav-link" href="#">Home <span class="sr-only">(current)</span></a>
           </li>
        <li class="nav-item">
            <a class="nav-link" href="#">Stats</a>
        </li>
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          Rankings
          </a>
          <div class="dropdown-menu" aria-labelledby="navbarDropdown">
          <a class="dropdown-item" href="#">Action</a>
          <a class="dropdown-item" href="#">Another action</a>
          <div class="dropdown-divider"></div>
          <a class="dropdown-item" href="#">Something else here</a>
          </div>
        </li>
          <li class="nav-item">
        </li>
        </ul>
        <form class="form-inline my-2 my-lg-0">
           <input class="form-control mr-sm-2" type="search" placeholder="Search Player Name" aria-label="Search">
           <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
        </form>
      </div>
    </nav>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <style>
    .navbar-brand{
      font-weight:bold;
      padding:2px;
      font-size: x-large; 
    }
    .block-container{
        background-image: url('https://res.cloudinary.com/people-matters/image/upload/q_auto,f_auto/v1665723752/1665723750.jpg');
        font-family: Arial, sans-serif;
        background-repeat: round;
    }
    
    .css-16idsys p {
    word-break: break-word;
    margin-bottom: 0px;
    font-size: 19px;
    font-weight: bold;
    }
    
    .css-10trblm{
      position: absolute;
      left: 163px;        
      top: -19px;
      font-weight:bold;
      color:coral;
    }
    
    .navbar{
     position: absolute;
     top: -55px;
    }
    .st-bd {
        padding: 1rem;
    }
    .st-btn {
        background-color: #4caf50;
        color: white;
        padding: 0.5rem 1rem;
        border: none;
        cursor: pointer;
        border-radius: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

teams=[
    'Sunrisers Hyderabad',
    'Mumbai Indians',
    'Royal Challengers Bangalore',
    'Kolkata Knight Riders',
    'Kings XI Punjab',
    'Chennai Super Kings',
    'Rajasthan Royals',
    'Delhi Capitals'
]

cities = ['Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi', 'Hyderabad',
       'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth',
       'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
       'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
       'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
       'Sharjah', 'Mohali', 'Bengaluru']

pipe = pickle.load(open('pipe.pkl', 'rb'))

st.title('IPL WIN PREDICTOR')


col1, col2 = st.columns(2)

with col1:
    batting_team=st.selectbox('Select the batting team',sorted(teams))
with col2:
    bowling_team=st.selectbox('Select the bowling team',sorted(teams))
selected_city = st.selectbox('Select host city', sorted(cities))

target = st.number_input('Target')
col3, col4, col5 = st.columns(3)

with col3:
    score= st.number_input('Score')
with col4:
    overs = st.number_input('Overs Completed')
with col5:
    wickets = st.number_input('Wickets Lost')

if st.button('Predict Win Probability'):
    runs_left = target - score
    balls_left = 120 - (overs*6)
    wickets = 10 - wickets
    crr = score/overs
    rrr = (runs_left*6)/ balls_left

input_df = pd.DataFrame({'batting_team':[batting_team],'bowling_team':[bowling_team],'city':[selected_city],'runs_left':[runs_left],'balls_left':[balls_left],'wickets':[wickets],'total_runs_x':[target],'crr':[crr],'rrr':[rrr]})
result = pipe.predict_proba(input_df)
loss = result[0][0]
win = result[0][1]
st.header(batting_team + "- " + str(round(win * 100)) + "%")
st.header(bowling_team + "- " + str(round(loss * 100)) + "%")
