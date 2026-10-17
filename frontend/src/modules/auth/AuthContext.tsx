import {
  createContext,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from "react";
import {
  clearSession,
  fetchCurrentUser,
  hasSession,
  signIn,
  readApiError,
  type ApiErrorBody,
  type AuthUser,
} from "../../shared/api/client";

interface AuthContextValue {
  user: AuthUser | null;
  loading: boolean;
  authError: ApiErrorBody | undefined;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [loading, setLoading] = useState(true);
  const [authError, setAuthError] = useState<ApiErrorBody>();

  useEffect(() => {
    let active = true;

    if (!hasSession()) {
      setLoading(false);
      return () => {
        active = false;
      };
    }

    fetchCurrentUser()
      .then((currentUser) => {
        if (active) setUser(currentUser);
      })
      .catch((error: unknown) => {
        const body = readApiError(error);
        if (body?.status === 401) clearSession();
        else if (active) setAuthError(body);
      })
      .finally(() => {
        if (active) setLoading(false);
      });

    return () => {
      active = false;
    };
  }, []);

  useEffect(() => {
    function handleUnauthorized() {
      clearSession();
      setUser(null);
      setAuthError(undefined);
    }

    window.addEventListener("qldt:unauthorized", handleUnauthorized);
    return () => window.removeEventListener("qldt:unauthorized", handleUnauthorized);
  }, []);

  async function login(username: string, password: string) {
    setUser(await signIn(username, password));
    setAuthError(undefined);
  }

  function logout() {
    clearSession();
    setUser(null);
    setAuthError(undefined);
  }

  return (
    <AuthContext.Provider value={{ user, loading, authError, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used within AuthProvider");
  return context;
}