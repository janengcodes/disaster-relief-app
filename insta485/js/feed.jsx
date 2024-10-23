import React, { useEffect, useState } from "react";
import PropTypes from "prop-types";
import InfiniteScroll from "react-infinite-scroll-component";
import Post from "./post";

export default function Feed({ url }) {
  const [data, setData] = useState([]);
  const [next, setNext] = useState("");
  const [dataFetched, setDataFetched] = useState(false);

  function fetchData(ignoreStaleRequest, urlForPosts) {
    // Call REST API to get the post's information
    fetch(urlForPosts, { credentials: "same-origin" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((responseData) => {
        if (!ignoreStaleRequest) {
          setData([...data, ...responseData.results]);
          setNext(responseData.next);
          setDataFetched(true);
        }
      })
      .catch((error) => console.log(error));
  }

  useEffect(() => {
    // Declare a boolean flag that we can use to cancel the API request.
    let ignoreStaleRequest = false;
    fetchData(ignoreStaleRequest, url);

    return () => {
      ignoreStaleRequest = true;
    };
  }, [url]);

  if (!dataFetched) {
    return <h1>Loading...</h1>;
  }

  return (
    <div>
      <InfiniteScroll
        dataLength={data.length}
        next={() => fetchData(false, next)}
        hasMore={next !== ""}
        loader={<h4>Loading...</h4>}
      >
        {data.map((post) => (
          <Post key={post.postid} url={post.url} />
        ))}
      </InfiniteScroll>
    </div>
  );
}

Feed.propTypes = {
  url: PropTypes.string.isRequired,
};
