"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { toast } from "sonner";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { cclient } from "@/api-sdk";
import { login } from "@/app/actions/auth";

const formSchema = z.object({
  user_id: z.string().min(1, "User ID is required"),
  password: z.string().min(1, "Password is required"),
});

export default function Login() {
  const { mutateAsync } = cclient.useMutation("post", "/v0/auth/token");

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      user_id: "",
      password: "",
    },
  });

  function onSubmit(data: z.infer<typeof formSchema>) {
    const mutationPromise = mutateAsync({
      body: {
        grant_type: "password",
        username: data.user_id,
        password: data.password,
        scope: "",
        client_id: null,
        client_secret: null,
      },
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      bodySerializer: (body) => {
        const formData = new URLSearchParams();
        Object.entries(body).forEach(([key, value]) => {
          if (value !== null && value !== undefined) {
            formData.append(key, value);
          }
        });
        return formData.toString();
      },
    });

    toast.promise(mutationPromise, {
      loading: "Logging in...",
      success: (response) => {
        login(response.access_token);
        return "Successfully logged in! Redirecting...";
      },
      error: () => "Login failed. Please check your credentials and try again.",
    });
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-100 font-sans dark:bg-black">
      <Card className="max-w-96">
        <CardHeader>
          <CardTitle>Login</CardTitle>
          <CardDescription>
            Bitte melden Sie sich mit Ihren Zugangsdaten an.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Form {...form}>
            <form
              onSubmit={form.handleSubmit(onSubmit)}
              className="flex flex-col space-y-8"
            >
              <FormField
                control={form.control}
                name="user_id"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>User ID</FormLabel>
                    <FormControl>
                      <Input placeholder="00000" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="password"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Passwort</FormLabel>
                    <FormControl>
                      <Input
                        placeholder="••••••••"
                        type="password"
                        {...field}
                      />
                    </FormControl>
                    <FormDescription>
                      Wenn Sie Ihr Passwort vergessen haben, wenden Sie sich
                      bitte an einen Administrator.
                    </FormDescription>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <Button type="submit">Einloggen</Button>
            </form>
          </Form>
        </CardContent>
      </Card>
    </div>
  );
}
