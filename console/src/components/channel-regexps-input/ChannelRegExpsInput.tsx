import React from 'react';
import Autocomplete from '@material-ui/lab/Autocomplete';
import TextField from '@material-ui/core/TextField';

type IgnoreChannelsInputProps = {
  value: string[];
  disabled: boolean;
  onChange: (channelRegExps: string[]) => void;
}

export default function ChannelRegExpsInput(props: IgnoreChannelsInputProps) {

  return (
    <div className="ChannelRegExpsInput">
      <Autocomplete<string>
        multiple
        freeSolo={true}
        disabled={props.disabled}
        value={props.value}
        onChange={(_, values) => props.onChange(values)}
        renderInput={params => (
          <TextField
            {...params}
            fullWidth
            label="Channel RegExps"
            placeholder="RegExp"
          />
        )}
      />
    </div>
  );
}
