import React, { useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { connect } from 'react-redux';
import { fetchProfile, UserProfile } from '../../redux/actions/profile';
import { StoreState } from '../../redux/reducers/root';
import { Box, TextField, Avatar, Input, Button } from '@mui/material';
import './login.css';
import { serverUrl } from '../../utils/constants';
import axios from 'axios';
import { Account, fetchAcc } from '../../redux/actions/account';

interface Props {
  profile: UserProfile;
  acc: Account;
  fetchAcc(): any;
}

function _Login(props: Props): JSX.Element {
  let navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState(false);

  async function login(username: string, password: string) {
    let response = await axios({
      data: { username: username, password: password },
      method: 'post',
      withCredentials: true,
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
      url: serverUrl + 'auth/login',
    });
    if (response.status === 200) {
      if (response.data.status === 'unauthorized') {
        setMessage(true);
      } else {
        props.fetchAcc();
        navigate('/');
      }
    }
  }
  return (
    <div>
      <nav>
        <Box position={'fixed'} className='nav'>
          <p className='logo-login'>LOGO</p>
        </Box>
        <Box className='login-box'>
          <p className='or'>{message ? 'Wrong username or password' : ''}</p>
          <Input
            color='primary'
            className='input-box'
            placeholder='Username'
            onChange={(event) => {
              setUsername(event.target.value);
            }}
          />
          <Input
            color='primary'
            className='input-box'
            placeholder='Password'
            onChange={(event) => {
              setPassword(event.target.value);
            }}
          />

          <div className='login-btn'>
            <Button
              fullWidth={true}
              variant='contained'
              onClick={() => {
                login(username, password);
              }}
            >
              Log In
            </Button>
          </div>
          <p className='or'>OR</p>
          <div className='signup'>
            <Button
              fullWidth={true}
              variant='contained'
              onClick={() => {
                navigate('/signup');
              }}
            >
              Sign up
            </Button>
          </div>
          <div className='forgot'>
            <Link to='/account/password/reset'>Forgot password?</Link>
          </div>
          <br />
          <br />
        </Box>
      </nav>
    </div>
  );
}

const mapStateToProps = (
  state: StoreState
): { profile: UserProfile; acc: Account } => {
  return { profile: state.profile, acc: state.acc };
};

export const Login = connect(mapStateToProps, { fetchAcc })(_Login);
