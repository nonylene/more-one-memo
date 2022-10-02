import React, { useState, useEffect } from 'react';
import Autocomplete, { createFilterOptions } from '@mui/material/Autocomplete';
import TextField from '@mui/material/TextField';

import { Channel, ChannelID } from '../../models/models';
import { getSlackChannels } from '../../apiClient'

type IgnoreChannelsInputProps = {
  value: ChannelID[];
  disabled: boolean;
  onChange: (channelIds: ChannelID[]) => void;
}

export default function IgnoreChannelsInput(props: IgnoreChannelsInputProps) {

  const [channelMap, setChannelMap] = useState<Map<ChannelID, Channel>>(new Map());
  const [loading, setLoading] = useState(false);

  const getChannelLabel = (opt: ChannelID) => {
    const channel = channelMap.get(opt);
    if (channel == null) {
      return opt
    }

    return `#${channel.name} | ${channel.id}`
  }

  // Use channel name to filter
  const filterOption = createFilterOptions({ stringify: getChannelLabel })

  useEffect(() => {
    setLoading(true);
    getSlackChannels()
      .then(channels => {
        const map = new Map(channels.map(c => [c.id, c]))
        setChannelMap(map)
      })
      .then(() => setLoading(false))
      .catch(console.log);
  }, []);

  return (
    <div className="IgnoreChannelsInput">
      <Autocomplete
        multiple
        options={Array.from(channelMap.keys())}
        loading={loading}
        disabled={props.disabled}
        loadingText="Loading Slack channels..."
        getOptionLabel={getChannelLabel}
        filterOptions={filterOption}
        value={props.value}
        onChange={(_, values) => props.onChange(values)}
        renderInput={params => (
          <TextField
            {...params}
            label="Ignore channels"
            placeholder="Channel"
            fullWidth />
        )}
      />
    </div>
  );
}
