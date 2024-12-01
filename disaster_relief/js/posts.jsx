import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import utc from "dayjs/plugin/utc";

dayjs.extend(relativeTime);
dayjs.extend(utc);

export function Posts({ postUrls }) {
    return (
      <div className="posts">
        {postUrls.map((url, index) => (
          <Post key={index} url={url} />
        ))}
      </div>
    );
  }