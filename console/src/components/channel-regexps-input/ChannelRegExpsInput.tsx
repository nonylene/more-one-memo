import React from 'react';
import Autocomplete from '@mui/material/Autocomplete';
import TextField from '@mui/material/TextField';

type IgnoreChannelsInputProps = {
  value: string[];
  disabled: boolean;
  onChange: (channelRegExps: string[]) => void;
}

export default function ChannelRegExpsInput(props: IgnoreChannelsInputProps) {

  return (
    <div className="ChannelRegExpsInput">
      <Autocomplete<string, true, undefined, true>
        multiple={true}
        freeSolo={true}
        disabled={props.disabled}
        options={[]}
        value={props.value}
        onChange={(_, values) => props.onChange(values)}
        renderInput={params => (
          <TextField
            {...params}
            fullWidth
            label="Channel RegExps"
            placeholder="RegExp" />
        )}
      />
    </div>
  );
}
