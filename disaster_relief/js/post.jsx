import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import utc from "dayjs/plugin/utc";

dayjs.extend(relativeTime);
dayjs.extend(utc);

// The parameter of this function is an object with a string called url inside it.
// url is a prop for the Post component.
export default function Post({ url }) {
  /* Display image and post owner of a single post */

  const [imgUrl, setImgUrl] = useState("");
  const [owner, setOwner] = useState("");
  const [comments, setComments] = useState([]);
  const [likes, setLikes] = useState(0);
  const [likeUrl, setLikeUrl] = useState("hello there");
  const [ownerImgUrl, setOwnerImgUrl] = useState("");
  const [postid, setPostid] = useState(0);
  const [commentText, setCommentText] = useState("");
  const [dataFetched, setDataFetched] = useState(false);
  const [created, setCreated] = useState("");

  useEffect(() => {
    // Declare a boolean flag that we can use to cancel the API request.
    let ignoreStaleRequest = false;

    // Call REST API to get the post's information
    fetch(url, { credentials: "same-origin" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        // If ignoreStaleRequest was set to true, we want to ignore the results of the
        // the request. Otherwise, update the state to trigger a new render.
        if (!ignoreStaleRequest) {
          setImgUrl(data.imgUrl);
          setOwner(data.owner);
          setComments(data.comments);
          setLikes(data.likes);
          setLikeUrl(data.likes.url);
          setOwnerImgUrl(data.ownerImgUrl);
          setPostid(data.postid);
          setDataFetched(true);
          setCreated(data.created);
        }
      })
      .catch((error) => console.log(error));

    return () => {
      // This is a cleanup function that runs whenever the Post component
      // unmounts or re-renders. If a Post is about to unmount or re-render, we
      // should avoid updating state.
      ignoreStaleRequest = true;
    };
  }, [url]);

  function toggleLikes(likesUrl) {
    if (likes.lognameLikesThis) {
      fetch(likesUrl, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          setLikes({ numLikes: likes.numLikes - 1, lognameLikesThis: false });
        })
        .catch((error) => console.log(error));
    } else {
      // const postData = {
      //   url: likesUrl,
      // };
      const modifiedUrl = `/api/v1/likes/?postid=${postid}`;
      // Send a POST request to the API
      fetch(modifiedUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        // body: JSON.stringify(postData),
      })
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          return response.json(); // Parse the JSON response
        })
        .then((data) => {
          setLikes({ numLikes: likes.numLikes + 1, lognameLikesThis: true });
          setLikeUrl(data.url);
        })
        .catch((error) => console.log(error));
    }
  }

  function deleteComment(commentid) {
    const modifiedUrl = `/api/v1/comments/${commentid}/`;
    fetch(modifiedUrl, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        setComments(
          comments.filter((comment) => comment.commentid !== commentid),
        );
      })
      .catch((error) => console.log(error));
  }

  function handleSubmit(e) {
    // Prevent the browser from reloading the page
    e.preventDefault();

    // Read the form data
    const form = e.target;
    const formData = new FormData(form);
    const myInputValue = formData.get("myInput");

    const modifiedUrl = `/api/v1/comments/?postid=${postid}`;

    const commentData = {
      text: myInputValue,
      postid, // Replace with the appropriate post ID
    };

    // Send a POST request to the API
    fetch(modifiedUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(commentData),
    })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json(); // Parse the JSON response
      })
      .then((data) => {
        // Update the comments state by adding the new comment
        setComments([...comments, data]);
      })
      .catch((error) => {
        // Handle errors if the POST request fails
        console.log(error);
      });

    // Optionally, clear the comment input field after submission
    setCommentText("");
  }

  if (!dataFetched) {
    return (
      <div className="posts">
        <h1>Loading...</h1>
      </div>
    );
  }

  function handleDoubleClick() {
    if (!likes.lognameLikesThis) {
      toggleLikes(likeUrl);
    }
  }
  // Generate a human-readable time stamp
  const timeCreated = dayjs.utc(created).local().fromNow();

  // Render post image and post owner
  return (
    <div className="posts">
      <div className="post">
        <div className="user">
          <img src={ownerImgUrl} alt="profile_picture" />
          <a href={`/users/${owner}/`}>
            <p>{owner}</p>
          </a>
          <a href={`/posts/${postid}/`}>{timeCreated}</a>
        </div>

        <div className="pic">
          <img
            src={imgUrl}
            alt="post_image"
            onDoubleClick={handleDoubleClick}
          />
        </div>
        {/* loop through the comments for each post */}
        <div className="likes">
          {likes.numLikes === 1
            ? `${likes.numLikes} like`
            : `${likes.numLikes} likes`}
        </div>
        <div className="likeButton" />
        <div>
          <button
            type="button"
            data-testid="like-unlike-button"
            onClick={() => toggleLikes(likeUrl)}
          >
            {likes.lognameLikesThis ? "Unlike" : "Like"}
          </button>
        </div>
        <div className="comments">
          {comments.map((comment) => (
            <div key={comment.commentid}>
              <p>
                <a href={`/users/${comment.owner}/`}>
                  <b>{comment.owner}</b>
                </a>
              </p>
              <span data-testid="comment-text">{comment.text}</span>
              <p>
                {comment.lognameOwnsThis && (
                  <button
                    type="button"
                    data-testid="delete-comment-button"
                    onClick={() => deleteComment(comment.commentid)}
                  >
                    Delete
                  </button>
                )}
              </p>
            </div>
          ))}
          <form data-testid="comment-form" onSubmit={handleSubmit}>
            <input
              type="text"
              name="myInput"
              value={commentText}
              onChange={(e) => setCommentText(e.target.value)}
            />
          </form>
        </div>
      </div>
    </div>
  );
}

Post.propTypes = {
  url: PropTypes.string.isRequired,
};