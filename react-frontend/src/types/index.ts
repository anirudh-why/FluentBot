export type ButtonProps = {
  label: string;
  onClick: () => void;
};

export type HeaderProps = {
  title: string;
  links?: { name: string; path: string }[];
};

export type PageProps = {
  children: React.ReactNode;
};