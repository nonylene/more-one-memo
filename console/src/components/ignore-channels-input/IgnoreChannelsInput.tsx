import React, { useState, useEffect } from 'react';
import Autocomplete from '@material-ui/lab/Autocomplete';
import TextField from '@material-ui/core/TextField';

import { Channel } from '../../models/models';
import { getSlackChannels } from '../../apiClient'

const channelToLabel = (channel: Channel) => `#${channel.name} | ${channel.id}`

export default function IgnoreChannelsInput() {

  const [channels, setChannels] = useState<Channel[]>([]);
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
        value={channels}
        onChange={(_, values) => setChannels(values)}
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
