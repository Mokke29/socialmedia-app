import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { connect } from 'react-redux';
import { fetchProfile, UserProfile } from '../../redux/actions/profile';
import { StoreState } from '../../redux/reducers/root';
import { Box, TextField, Avatar, Button } from '@mui/material';
import './home.css';
import { serverUrl } from '../../utils/constants';
import { FollowTheSigns } from '@mui/icons-material';
import axios from 'axios';
import { Account, fetchAcc } from '../../redux/actions/account';
import useInfiniteScroll from './useInfiniteScroll';
import { ViewPost } from '../../components/post/ViewPost';

interface Props {
  profile: UserProfile;
  acc: Account;
  fetchProfile(profileName?: string): any;
  fetchAcc(): any;
}

interface FollowedPosts {
  likes: number;
  comments: number;
  id: number;
  creator: string;
  image_path: string;
  content: string;
  avatar: string;
}

interface Profiles {
  id: number;
  avatar_path: string;
  profile_name: string;
}

function _Home(props: Props): JSX.Element {
  const [data, setData] = useState<Array<FollowedPosts>>([]);
  const [page, setPage] = useState(1);
  const [isFetching, setIsFetching] = useInfiniteScroll(moreData);
  const [postInfo, setPostInfo] = useState(false);
  const [viewPost, setViewPost] = useState(false);
  const [postId, setPostId] = useState(0);
  const [suggestedProfiles, setSuggestedProfiles] = useState<Array<Profiles>>(
    []
  );

  const loadData = () => {
    axios({
      method: 'get',
      withCredentials: true,
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
      url: serverUrl + 'post/get/followed/1',
    })
      .then((response) => {
        setData(response.data.posts);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const loadSuggested = () => {
    axios({
      method: 'get',
      withCredentials: true,
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
      url: serverUrl + 'profile/suggested',
    })
      .then((response) => {
        setSuggestedProfiles(response.data.profiles);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  function moreData() {
    axios({
      method: 'get',
      withCredentials: true,
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
      url: serverUrl + `post/get/followed/${page}?sort=latest`,
    })
      .then((response) => {
        setData([...data, ...response.data.posts]);
        setPage(page + 1);
        setIsFetching(false);
      })
      .catch((error) => {
        console.log(error);
      });
  }

  useEffect(() => {
    loadData();
    loadSuggested();
  }, []);

  if (data.length === 0) {
    return <h1>Loading...</h1>;
  }

  return (
    <div className='home-container'>
      <ul className='posts-ul'>
        {data.map((x, key) => (
          <li className='post-li' key={x.id}>
            <div className='avatar-name'>
              <Avatar
                className='avatar-home'
                alt='User avatar'
                src={`${serverUrl}static/avatar/${x.avatar}`}
                sx={{ width: 35, height: 35 }}
              />
              <a href={`${x.creator}`} className='post-creator-name'>
                {x.creator}
              </a>
            </div>
            <img
              onClick={() => {
                setViewPost(true);
                setPostId(x.id);
              }}
              onMouseEnter={(e) => {
                setPostInfo(true);
              }}
              onMouseLeave={(e) => {
                setPostInfo(false);
              }}
              className='post-img-home'
              src={`${serverUrl}static/posts/${x.image_path}`}
              alt=''
            ></img>
            <p className='post-likes'>{x.likes} likes</p>
            <p className='post-content'>{x.content}</p>
          </li>
        ))}
      </ul>
      <ul className='suggested-profiles-ul'>
        <p className='suggestions-for-you'>Suggestions For You</p>
        {suggestedProfiles.map((profile, key) => (
          <li className='suggest-li' key={profile.id}>
            <div className='avatar-name'>
              <Avatar
                className='avatar-home'
                alt='User avatar'
                src={`${serverUrl}static/avatar/${profile.avatar_path}`}
                sx={{ width: 35, height: 35 }}
              />
              <div className='suggest-name'>
                <a className='suggest-link' href={`${profile.profile_name}`}>
                  {profile.profile_name}
                </a>
                <p className='suggest-follow-link'>Follow</p>
              </div>
            </div>
          </li>
        ))}
      </ul>
      <div>
        {viewPost ? (
          <ViewPost setViewPost={setViewPost} id={postId}></ViewPost>
        ) : (
          ''
        )}
      </div>
    </div>
  );
}

const mapStateToProps = (
  state: StoreState
): { profile: UserProfile; acc: Account } => {
  return { profile: state.profile, acc: state.acc };
};

export const Home = connect(mapStateToProps, { fetchProfile, fetchAcc })(_Home);
