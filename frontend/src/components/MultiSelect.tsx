import * as React from "react";
import { Check, ChevronsUpDown, X } from "lucide-react";
import { Button } from "./ui/button";
import { Badge } from "./ui/badge";
import { Popover, PopoverContent, PopoverTrigger } from "./ui/popover";
import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList } from "./ui/command";
import { cn } from "../lib/utils";

type Props = {
  label: string;
  options: string[];
  value: string[];
  onChange: (next: string[]) => void;
  placeholder?: string;
};

export default function MultiSelect({ label, options, value, onChange, placeholder="Select..." }: Props) {
  const [open, setOpen] = React.useState(false);

  function toggle(v: string) {
    if (value.includes(v)) onChange(value.filter(x => x !== v));
    else onChange([...value, v]);
  }

  function clear() {
    onChange([]);
  }

  return (
    <div className="space-y-1">
      <div className="text-xs font-medium text-black/70">{label}</div>
      <Popover open={open} onOpenChange={setOpen}>
        <PopoverTrigger asChild>
          <Button variant="outline" className="w-full justify-between">
            <span className={cn("truncate", value.length ? "" : "text-black/50")}>
              {value.length ? value.join(", ") : placeholder}
            </span>
            <ChevronsUpDown className="ml-2 h-4 w-4 opacity-50" />
          </Button>
        </PopoverTrigger>
        <PopoverContent className="z-50 w-[320px] rounded-md border border-black/10 bg-white p-0 shadow-lg">
          <Command>
            <CommandInput placeholder={`Search ${label}...`} />
            <CommandList>
              <CommandEmpty className="p-3 text-sm text-black/60">No results.</CommandEmpty>
              <CommandGroup>
                {options.map((opt) => (
                  <CommandItem key={opt} value={opt} onSelect={() => toggle(opt)}>
                    <div className="mr-2 flex h-4 w-4 items-center justify-center rounded border border-black/20">
                      {value.includes(opt) ? <Check className="h-3 w-3" /> : null}
                    </div>
                    <span className="truncate">{opt}</span>
                  </CommandItem>
                ))}
              </CommandGroup>
            </CommandList>
          </Command>

          <div className="flex items-center justify-between border-t border-black/10 p-2">
            <Button variant="ghost" size="sm" onClick={clear} disabled={!value.length}>
              <X className="mr-1 h-4 w-4" /> Clear
            </Button>
            <Button size="sm" onClick={() => setOpen(false)}>Done</Button>
          </div>
        </PopoverContent>
      </Popover>

      {value.length ? (
        <div className="flex flex-wrap gap-1 pt-1">
          {value.map(v => (
            <Badge key={v} className="gap-1">
              {v}
              <button className="ml-1 opacity-60 hover:opacity-100" onClick={() => toggle(v)}>×</button>
            </Badge>
          ))}
        </div>
      ) : null}
    </div>
  );
}
