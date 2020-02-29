import React, { useState, useEffect } from 'react';
import Autocomplete from '@material-ui/lab/Autocomplete';
import TextField from '@material-ui/core/TextField';

import { Channel } from '../../models/models';
import { getSlackChannels } from '../../apiClient'

type IgnoreChannelsInputProps = {
  value: Channel[];
  onChange: (channels: Channel[]) => void;
}

const channelToLabel = (channel: Channel) => `#${channel.name} | ${channel.id}`

export default function IgnoreChannelsInput(props: IgnoreChannelsInputProps) {

  const [allChannels, setAllChannels] = useState<Channel[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    getSlackChannels()
      .then(setAllChannels).then(() => setLoading(false))
      .catch(console.log);
  }, []);

  return (
    <div className="IgnoreChannelsInput">
      <Autocomplete
        multiple
        options={allChannels}
        loading={loading}
        loadingText="Loading Slack channels..."
        getOptionLabel={channelToLabel}
        value={props.value}
        onChange={(_, values) => props.onChange(values)}
        renderInput={params => (
          <TextField
            {...params}
            label="Ignore channels"
            placeholder="Channels"
            fullWidth
          />
        )}
      />
    </div>
  );
}
